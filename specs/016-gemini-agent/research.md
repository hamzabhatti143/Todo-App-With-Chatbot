# Research: Gemini AI Agent for Task Management

**Branch**: `016-gemini-agent` | **Date**: 2026-01-17 | **Phase**: 0 - Research

## Research Context

This research phase resolves open questions before designing and implementing the TodoBot agent. The goal is to determine the optimal technical approach for integrating Gemini 2.0 Flash with the existing MCP Task Server tools.

## Research Task 1: Gemini API Function Calling Patterns

**Question**: How does Gemini 2.0 Flash support function calling, and what is the API pattern?

### Findings from Existing Implementation

Examined `backend/app/services/gemini_service.py` (Feature 013) which already implements Gemini function calling:

**Current Implementation Pattern**:
```python
from google.generativeai import GenerativeModel

# 1. Define tools as Python dictionaries (function declarations)
tools = [
    {
        "name": "add_task",
        "description": "Create a new task",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "User UUID"},
                "title": {"type": "string", "description": "Task title"}
            },
            "required": ["user_id", "title"]
        }
    }
]

# 2. Create model with tools
model = GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config={"temperature": 0.7, "max_output_tokens": 2048},
    tools=tools
)

# 3. Start chat session with history
chat = model.start_chat(history=previous_messages)

# 4. Send message and get response
response = chat.send_message(user_message)

# 5. Check for function calls
if hasattr(response, "function_calls") and response.function_calls:
    for func_call in response.function_calls:
        tool_name = func_call.name
        arguments = dict(func_call.args)
        # Execute the tool
        result = await execute_tool(tool_name, arguments)
```

**Key Insights**:
- Gemini uses OpenAPI-style function declarations (similar to OpenAI format)
- Tools are passed at model initialization, not per-request
- Function calls are returned in `response.function_calls`
- Arguments are accessible via `func_call.args` (dict-like object)
- Multiple function calls can be returned in one response

**Decision**: Use Gemini's native function calling API (already proven in Feature 013)

---

## Research Task 2: Framework Decision - Direct SDK vs OpenAI Agents SDK

**Question**: Should we use OpenAI Agents SDK or direct google-generativeai SDK?

### OpenAI Agents SDK Analysis

**What is it**: Framework by OpenAI for building stateful agents with tool calling, conversation memory, and workflow orchestration.

**Compatibility with Gemini**:
- ❌ Designed specifically for OpenAI models (GPT-4, GPT-3.5)
- ❌ Uses OpenAI's API format and authentication
- ❌ Would require adapter layer to translate to Gemini API
- ❌ No official Gemini support or examples

**Conclusion**: OpenAI Agents SDK is NOT compatible with Gemini 2.0 Flash

### Direct google-generativeai SDK Analysis

**Advantages**:
1. ✅ Already installed and used in Feature 013 (version 0.8.3)
2. ✅ Native Gemini API support with all features
3. ✅ Proven pattern in existing codebase (gemini_service.py)
4. ✅ Direct access to function calling API
5. ✅ No adapter layer needed
6. ✅ Simple, maintainable implementation

**Disadvantages**:
1. ❌ No built-in agent framework (we build our own)
2. ❌ Manual conversation history management
3. ❌ Manual tool execution orchestration

**Decision**: Use direct google-generativeai SDK (version 0.8.3)

**Rationale**:
- Existing codebase already has working Gemini integration
- Building a simple agent wrapper is straightforward (~300 lines)
- No external dependencies on unsupported frameworks
- Aligns with constitution's principle of simplicity

---

## Research Task 3: Task Identification from Natural Language

**Question**: How do we match natural language references ("the groceries task") to task IDs?

### Challenge

Users will say things like:
- "Mark the groceries task as done"
- "Delete that shopping task"
- "Update the report task"

But MCP tools require task UUIDs, not natural language descriptions.

### Approach Options

**Option A: Require Exact Task ID**
- User must provide UUID: "Complete task 7c9e6679-7425-40de-944b-e07fc1f90ae7"
- ❌ Poor UX, defeats purpose of natural language
- ✅ No ambiguity

**Option B: List Tasks First Pattern**
- Agent always calls `list_tasks` before operations requiring task_id
- User sees numbered list: "1. Buy groceries, 2. Call mom"
- User references by number: "Complete task 1"
- Agent maps number to task_id from recent list
- ✅ Clear mapping
- ❌ Extra API call overhead
- ❌ Agent must maintain context of recent list

**Option C: Title Matching with Clarification**
- Agent calls `list_tasks` to get all tasks
- Agent performs fuzzy matching on task titles
- If single match found: proceed with operation
- If multiple matches: ask user to clarify
- If no match: inform user task not found
- ✅ Natural language friendly
- ✅ Handles ambiguity gracefully
- ❌ Extra API call for every operation

**Option D: Hybrid - Smart Context**
- Agent maintains conversation context about recently discussed tasks
- When user says "that task" or "the task", refer to most recent task mentioned
- When user provides title fragment, use Option C (title matching)
- ✅ Best UX for conversational flow
- ❌ Most complex to implement
- ❌ Context management challenges

### Decision: Option C - Title Matching with Clarification

**Rationale**:
1. Balances UX and implementation complexity
2. Aligns with FR-015 in spec: "Agent MUST identify tasks by title matching when user doesn't provide task ID"
3. Gemini can handle fuzzy matching naturally
4. Clarification questions improve accuracy (FR-010)

**Implementation Pattern**:
```python
async def identify_task(user_id: str, task_reference: str) -> Optional[str]:
    """
    Identify task_id from natural language reference.

    Returns:
        - task_id if single match found
        - None if no match or multiple matches (agent will ask user)
    """
    # Get all user tasks
    tasks_response = await list_tasks(user_id, status="all")

    # Parse task list (agent has context)
    # Gemini performs fuzzy matching on titles
    # Returns task_id or asks for clarification
```

**Agent System Instructions**:
- "When user references a task by title, call list_tasks first"
- "Match the title fragment to task titles (case-insensitive)"
- "If multiple matches, ask user which task they mean"
- "If no matches, inform user no matching task found"

---

## Research Task 4: Conversation Context Management

**Question**: What format should conversation history use, and how many messages should we keep?

### Gemini Context Window

**Gemini 2.0 Flash Specifications**:
- Context window: 1,048,576 tokens (1M tokens)
- Output limit: 8,192 tokens

**Practical Limits**:
- Average message: ~100 tokens
- Tool calls with results: ~200-500 tokens
- 20 message turns ≈ 2,000-5,000 tokens (well within limits)

### History Format

**Gemini API Format**:
```python
history = [
    {"role": "user", "parts": ["Add buy groceries"]},
    {"role": "model", "parts": ["Task created: Buy groceries (ID: ...)"]},
    {"role": "user", "parts": ["Show my tasks"]},
    {"role": "model", "parts": ["Your tasks:\n◯ Buy groceries\n..."]},
]
```

**Key Requirements**:
- Role must be "user" or "model" (not "assistant")
- Parts is a list (supports multipart messages with images, etc.)
- Tool calls are represented differently (function_call and function_response parts)

### Message Retention Strategy

**Options**:

**Option A: Fixed Window (Last N messages)**
- Keep last 20 messages (10 turns)
- Drop older messages
- ✅ Simple implementation
- ✅ Predictable token usage
- ❌ Loses long-term context

**Option B: Token-Based Window**
- Keep messages until token limit reached
- Drop oldest messages first
- ✅ Efficient token usage
- ❌ Requires token counting
- ❌ More complex

**Option C: Semantic Summarization**
- Summarize old messages before dropping
- Keep recent messages verbatim
- ✅ Preserves important context
- ❌ Extra API call for summarization
- ❌ Complexity

### Decision: Option A - Fixed Window (20 messages)

**Rationale**:
1. Aligns with SC-007 success criteria: "Support 5+ consecutive turns" (20 messages = 10 turns)
2. Simple implementation, no token counting needed
3. 20 messages well within Gemini's 1M token limit
4. Caller can implement more sophisticated strategies if needed

**Implementation**:
```python
def prepare_conversation_context(
    messages: List[Dict[str, str]],
    max_messages: int = 20
) -> List[Dict[str, Any]]:
    """
    Convert conversation messages to Gemini format.

    Args:
        messages: List of {role: "user"|"assistant", content: str}
        max_messages: Maximum messages to keep (default 20)

    Returns:
        Gemini-formatted history (last max_messages)
    """
    # Take last N messages
    recent_messages = messages[-max_messages:] if len(messages) > max_messages else messages

    # Convert to Gemini format
    gemini_history = []
    for msg in recent_messages:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({
            "role": role,
            "parts": [msg["content"]]
        })

    return gemini_history
```

---

## Research Task 5: Error Handling Patterns

**Question**: How should the agent handle errors gracefully with user-friendly messages?

### Error Categories

**1. Gemini API Errors**
- Rate limiting (ResourceExhausted)
- Service unavailable
- Invalid API key
- Timeout

**2. MCP Tool Errors**
- Task not found
- Permission denied
- Validation errors (title too long, etc.)
- Database connection failures

**3. User Input Errors**
- Ambiguous requests
- Empty/nonsensical input
- Missing required information

**4. Agent Logic Errors**
- Unable to identify intent
- Multiple interpretations possible
- Unexpected response format

### Existing Error Handling (Feature 013)

From `gemini_service.py`:

```python
@retry_with_exponential_backoff(max_retries=3, initial_delay=1.0)
def generate_chat_response_with_tools(...):
    """Automatic retry with exponential backoff for API errors"""
    try:
        # Gemini API call
    except (
        google_exceptions.ResourceExhausted,
        google_exceptions.ServiceUnavailable,
        google_exceptions.DeadlineExceeded,
        google_exceptions.GoogleAPICallError,
    ) as e:
        logger.error(f"Error: {e}")
        raise
```

**Pattern**: Retry with exponential backoff, then propagate exception to caller

### Decision: Three-Tier Error Handling

**Tier 1: API-Level Errors (Retry)**
- Use existing `@retry_with_exponential_backoff` decorator
- Retry ResourceExhausted, ServiceUnavailable, DeadlineExceeded
- After 3 retries, convert to user-friendly message

**Tier 2: Tool Execution Errors (Wrap)**
- Catch ValueError from MCP tools
- Extract error message and provide context
- Example: "Task not found" → "I couldn't find that task. Please check the title and try again."

**Tier 3: Agent Logic Errors (Clarify)**
- When intent unclear, ask clarifying questions
- When multiple interpretations, present options
- Example: "Complete task" → "Which task would you like to complete? You have 3 pending tasks."

### Error Message Templates

```python
ERROR_MESSAGES = {
    # API Errors
    "rate_limit": "I'm receiving too many requests right now. Please try again in a moment.",
    "api_unavailable": "The AI service is temporarily unavailable. Please try again later.",
    "api_timeout": "The request took too long. Please try again.",
    "api_error": "I encountered an error processing your request. Please try again.",

    # Tool Errors
    "task_not_found": "I couldn't find a task matching '{reference}'. Could you be more specific?",
    "permission_denied": "You don't have permission to modify that task.",
    "validation_error": "Invalid input: {details}",
    "database_error": "I couldn't save your changes due to a database error. Please try again.",

    # User Input Errors
    "empty_input": "I didn't understand that. Could you please provide more details?",
    "ambiguous_request": "I found multiple tasks matching '{reference}'. Which one did you mean?",
    "missing_info": "I need more information. {what_is_missing}",

    # Agent Logic Errors
    "unclear_intent": "I'm not sure what you'd like me to do. Try asking me to add, list, complete, update, or delete tasks.",
    "unexpected_format": "I received an unexpected response. Please try rephrasing your request.",
}
```

### Implementation Pattern

```python
async def safe_tool_execution(
    tool_name: str,
    arguments: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Execute MCP tool with error handling.

    Returns:
        {"success": True, "result": str} or
        {"success": False, "error": str}
    """
    try:
        result = await execute_mcp_tool(tool_name, arguments)
        return {"success": True, "result": result}

    except ValueError as e:
        # Tool validation or permission errors
        error_msg = str(e)

        if "not found" in error_msg.lower():
            return {"success": False, "error": ERROR_MESSAGES["task_not_found"]}
        elif "permission denied" in error_msg.lower():
            return {"success": False, "error": ERROR_MESSAGES["permission_denied"]}
        else:
            return {"success": False, "error": f"Error: {error_msg}"}

    except Exception as e:
        # Unexpected errors
        logger.error(f"Unexpected error in {tool_name}: {e}")
        return {"success": False, "error": ERROR_MESSAGES["database_error"]}
```

---

## Summary of Research Findings

### Research Task 1: Function Calling ✅
- **Decision**: Use Gemini's native function calling API
- **Pattern**: Define tools as OpenAPI-style declarations, extract from `response.function_calls`
- **Reference**: Existing implementation in `gemini_service.py`

### Research Task 2: Framework ✅
- **Decision**: Use direct google-generativeai SDK (version 0.8.3)
- **Rationale**: Already installed, proven pattern, no adapter needed
- **Reject**: OpenAI Agents SDK (incompatible with Gemini)

### Research Task 3: Task Identification ✅
- **Decision**: Title matching with clarification (Option C)
- **Pattern**: Call `list_tasks` → fuzzy match → clarify if ambiguous
- **Implementation**: Agent system instructions + context management

### Research Task 4: Conversation Context ✅
- **Decision**: Fixed window of last 20 messages (10 turns)
- **Format**: Gemini format with "user"/"model" roles
- **Rationale**: Simple, within token limits, meets success criteria

### Research Task 5: Error Handling ✅
- **Decision**: Three-tier error handling (Retry → Wrap → Clarify)
- **Patterns**: Exponential backoff (API), user-friendly messages (tools), clarifying questions (logic)
- **Implementation**: Error message templates + safe tool execution wrapper

---

## Next Steps

With all research tasks completed, we can now proceed to:

**Phase 1: Design Artifacts**
1. Create `data-model.md` - Define agent configuration, request/response schemas
2. Create agent system instructions template (prompt engineering)
3. Define MCP tool declarations for Gemini
4. Create `quickstart.md` - Usage examples and integration guide

**Status**: ✅ Research Phase Complete
**Next Phase**: Phase 1 - Design Artifacts
**Estimated Duration**: ~30 minutes
