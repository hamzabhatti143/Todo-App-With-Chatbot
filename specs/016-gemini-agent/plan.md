# Implementation Plan: Gemini AI Agent for Task Management

**Branch**: `016-gemini-agent` | **Date**: 2026-01-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/016-gemini-agent/spec.md`

## Summary

Implement TodoBot, a conversational AI agent powered by Gemini 2.0 Flash that enables users to manage tasks through natural language. The agent integrates with the existing MCP Task Server (Feature 015) tools to provide a friendly alternative to the web UI, understanding commands like "add buy groceries", "show my tasks", and "mark the groceries task as done".

**Primary Requirement**: Natural language task management via Gemini AI agent
**Technical Approach**: Direct Gemini API integration (google-generativeai SDK) with MCP tools as function calls, avoiding OpenAI Agents SDK compatibility issues

## Technical Context

**Language/Version**: Python 3.11+ (existing backend environment)
**Primary Dependencies**:
- google-generativeai==0.8.3 (already installed for chat feature)
- Existing MCP tools from Feature 015
- python-dotenv for environment configuration

**Storage**: N/A (agent is stateless, conversation history passed by caller)
**Testing**: pytest with async support (pytest-asyncio)
**Target Platform**: Linux server (backend environment)
**Project Type**: Backend service (web application monorepo)

**Performance Goals**:
- Agent response time: P95 < 3 seconds (including Gemini API + tool execution)
- Tool call accuracy: 90% intent identification without clarification
- Conversation context: Support 20+ message turns

**Constraints**:
- Must integrate with existing MCP tools without modification
- Must enforce user isolation (user_id validation)
- Must handle Gemini API failures gracefully
- Must be stateless (no conversation storage in agent)

**Scale/Scope**:
- Single agent module (~300 lines)
- 5 MCP tools integrated
- Comprehensive test coverage for all user story scenarios

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Monorepo Organization - ✅ COMPLIANT

Agent located in `backend/app/agent.py` within existing backend structure.
No new top-level directories required.

### Principle II: Code Quality Standards - ✅ COMPLIANT

- Type hints mandatory: Agent functions will have full type annotations
- Function size: Each function < 30 lines (agent runner, tool wrapper helpers)
- DRY: Shared prompt templates and error handling utilities
- Error handling: Try-catch with user-friendly messages
- Naming: Clear function names (run_agent, create_agent_prompt, etc.)

### Principle III: Frontend Architecture - ⚠️ NOT APPLICABLE

This is backend-only feature. No frontend changes in this feature.

### Principle IV: Backend Architecture - ⚠️ PARTIAL DEVIATION

**Deviation**: Agent doesn't use REST API patterns (it's a library, not endpoints)

**Justification**: Agent is a Python module consumed by other services (like chat API), not a REST endpoint itself. It follows Python module patterns, not HTTP patterns.

**Compliance**:
- ✅ Uses existing database through MCP tools (which use SQLModel)
- ✅ Uses Pydantic for input validation (conversation context, user input)
- ✅ Environment variables for API keys (GEMINI_API_KEY)
- ❌ Not REST endpoints (it's a callable module)
- ❌ Not HTTP status codes (returns Python objects/exceptions)

**Impact**: Low - Agent is backend utility, not exposed as HTTP API directly

### Principle V: Database Standards - ✅ COMPLIANT

Agent doesn't directly access database; uses existing MCP tools which already follow all database standards (SQLModel, Neon PostgreSQL, etc.)

### Principle VI: Authentication Architecture - ⚠️ PARTIAL DEVIATION

**Deviation**: Agent doesn't verify JWT tokens (assumes caller provides authenticated user_id)

**Justification**: Agent is internal library, not API endpoint. Caller (e.g., chat API endpoint) performs JWT verification and extracts user_id before calling agent.

**Security Model**:
- Agent receives user_id as parameter (trusted from caller)
- Agent passes user_id to MCP tools which enforce ownership
- MCP tools validate user can only access own tasks
- Authentication happens at HTTP layer, not agent layer

**Impact**: Medium - Requires documentation that agent must be called from authenticated context only

**Mitigation**: Document security requirements clearly, add input validation for user_id format (UUID validation)

### Principle VII: API Endpoint Structure - ⚠️ NOT APPLICABLE

Agent is not an API endpoint. It's a Python module called by other backend services.

### Principle VIII: Spec-Driven Development - ✅ COMPLIANT

Feature has full specification (spec.md)
This plan follows `/sp.plan` workflow
Tasks will be generated with `/sp.tasks`
Implementation will follow specification requirements

### Principle IX: Agent-Based Development - ✅ COMPLIANT

Will use @fastapi-backend-dev for implementation (Python backend code)
Will use @code-reviewer for validation
Agent is backend component, uses backend development patterns

### Principle X: Testing & Quality Gates - ✅ COMPLIANT

- Type Safety: Python type hints on all agent functions
- Linting: Ruff will validate code quality
- Code Review: @code-reviewer will validate against constitution
- Integration Test: Test agent with real MCP tools and mock Gemini responses
- Documentation: Will document agent API and usage patterns
- User Isolation: MCP tools enforce user_id ownership

## Project Structure

### Documentation (this feature)

```text
specs/016-gemini-agent/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0: Gemini API research
├── data-model.md        # Phase 1: Agent data structures
├── quickstart.md        # Phase 1: Usage guide
└── tasks.md             # Phase 2: Task breakdown (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/app/
├── agent.py             # NEW: TodoBot agent module
├── test_agent.py        # NEW: Agent tests
├── mcp_server/          # EXISTING: MCP tools (Feature 015)
│   ├── __init__.py
│   ├── tools.py         # 5 MCP tools: add_task, list_tasks, etc.
│   └── server.py
└── services/            # EXISTING: Chat service may call agent (future)
```

**Structure Decision**: Single-file module approach for agent. Agent is a simple Python module with one main function (`run_agent`) that accepts user input, user_id, and conversation history. All agent logic in one file keeps it simple and maintainable. Tests in separate file following pytest conventions.

## Complexity Tracking

**Justified Deviations**:

1. **Non-REST Module (Principle IV)**
   - **Complexity Score**: Low
   - **Why Needed**: Agent is utility library, not API endpoint; consumed by other services
   - **Simpler Alternative Rejected**: Making agent a REST endpoint would add unnecessary HTTP overhead and doesn't fit use case (called internally, not by external clients)
   - **Benefit**: Simpler integration, lower latency, easier to test
   - **Cost**: Different pattern than typical backend code (but well-established Python module pattern)

2. **No JWT Verification (Principle VI)**
   - **Complexity Score**: Low
   - **Why Needed**: Agent is internal library; JWT verification belongs at HTTP boundary, not in business logic
   - **Simpler Alternative Rejected**: Adding JWT verification to agent would violate separation of concerns (mixing HTTP auth with business logic)
   - **Benefit**: Cleaner separation of concerns, agent reusable from any authenticated context
   - **Cost**: Requires documentation and careful use (caller must authenticate)
   - **Mitigation**: Validate user_id format (UUID), document security requirements, add tests for user isolation

**Complexity Budget**:
- **Allocated**: 2 low-complexity deviations
- **Used**: 2 low-complexity deviations
- **Remaining**: 0
- **Status**: At budget limit for low-complexity; no medium/high complexity deviations allowed

## Phase 0: Research

### Research Task 1: Gemini API Function Calling

**Question**: How does Gemini 2.0 Flash support function calling for tool integration?

**Goal**: Determine the pattern for integrating MCP tools as Gemini function calls

**Research Questions**:
- What is the function calling API in google-generativeai SDK?
- How to define tool schemas for Gemini?
- How does Gemini return function call requests?
- How to handle function results in conversation flow?
- Are there limitations on number of tools or schema complexity?

**Method**: Review google-generativeai SDK documentation, examine existing chat feature code (013-todo-ai-chatbot)

**Deliverable**: research.md section on function calling patterns with code examples

### Research Task 2: OpenAI Agents SDK Compatibility

**Question**: Can we use OpenAI Agents SDK with Gemini 2.0 Flash, or should we use direct SDK?

**Goal**: Determine if OpenAI Agents SDK is compatible with Gemini or if we need different approach

**Research Questions**:
- Does OpenAI Agents SDK support Gemini models?
- Are there compatibility layers or wrappers?
- What are the trade-offs of using direct google-generativeai vs agents framework?
- Is there a Gemini-specific agents framework we should use instead?

**Method**: Search for OpenAI Agents SDK + Gemini integration examples, check SDK documentation

**Deliverable**: research.md section on framework decision with rationale

**Decision Preview**: Based on existing codebase using google-generativeai==0.8.3, likely to use direct SDK rather than OpenAI Agents SDK (which is designed for OpenAI models). This aligns with existing chat feature implementation.

### Research Task 3: Task Identification from Natural Language

**Question**: How should agent identify which task user is referring to when they say "mark the groceries task as done"?

**Goal**: Design pattern for matching natural language task references to task IDs

**Research Questions**:
- Should agent list tasks first, then ask user to pick by number?
- Should agent do fuzzy matching on task titles?
- Should agent maintain context of recently listed tasks?
- How to handle ambiguous references ("the task" when multiple exist)?

**Method**: Review natural language task management patterns, consider conversation flow

**Deliverable**: research.md section on task identification strategy with examples

### Research Task 4: Conversation Context Management

**Question**: How should conversation history be structured and passed to agent?

**Goal**: Define conversation context format and size limits

**Research Questions**:
- What message format does Gemini SDK expect?
- How many previous messages should be included?
- Should we summarize old context to fit window?
- How to include recent tool results in context?

**Method**: Review Gemini API context window docs, existing chat implementation

**Deliverable**: research.md section on context format with schema

### Research Task 5: Error Handling Patterns

**Question**: How should agent handle various failure scenarios gracefully?

**Goal**: Define error handling strategy for all edge cases from spec

**Research Questions**:
- How to handle Gemini API failures (rate limiting, timeout, errors)?
- How to communicate tool execution failures to user?
- How to ask for clarification on ambiguous input?
- What error messages are user-friendly vs technical?

**Method**: Review error scenarios from spec edge cases, design error response formats

**Deliverable**: research.md section on error handling with examples for each edge case

## Phase 1: Design Artifacts

### Artifact 1: Data Model (`data-model.md`)

**Agent Configuration**:
- Agent name: "TodoBot"
- Model identifier: "gemini-2.0-flash-exp"
- System instructions: Comprehensive prompt defining behavior
- Tools: List of MCP tool function definitions

**Conversation Context Structure**:
```python
{
  "user_id": "UUID string",
  "history": [
    {"role": "user", "content": "message text"},
    {"role": "assistant", "content": "response text"},
    ...
  ]
}
```

**Agent Response Structure**:
```python
{
  "response": "text response to user",
  "tool_calls": [
    {"tool": "add_task", "args": {...}},
    ...
  ],
  "requires_clarification": bool
}
```

### Artifact 2: Agent Instructions Template

System prompt defining TodoBot personality and capabilities:
- Friendly, conversational tone
- Use emoji for confirmations
- Ask for clarification when needed
- Understand natural language variations
- Map user intent to appropriate tools
- Handle errors gracefully

### Artifact 3: Tool Function Definitions

Map MCP tools to Gemini function calling schema:
- add_task(user_id, title, description) → Task creation
- list_tasks(user_id, status) → Task retrieval
- complete_task(user_id, task_id) → Mark complete
- delete_task(user_id, task_id) → Remove task
- update_task(user_id, task_id, title, description) → Modify task

### Artifact 4: Quickstart Guide (`quickstart.md`)

Usage examples:
- Basic agent invocation
- Passing conversation context
- Handling responses
- Testing with different intents
- Error scenario examples

## Phase 2: Implementation Steps

### Step 1: Gemini Client Setup (10 minutes)

**File**: `backend/app/agent.py`

**Tasks**:
1. Import google.generativeai library
2. Create `initialize_gemini()` function
3. Load API key from environment (GEMINI_API_KEY)
4. Configure Gemini client with safety settings
5. Return configured client
6. Add error handling for missing API key

**Deliverable**: Working Gemini client initialization function

### Step 2: Tool Schema Definition (15 minutes)

**File**: `backend/app/agent.py`

**Tasks**:
1. Import MCP tools from mcp_server
2. Create `get_tool_schemas()` function
3. Map each MCP tool to Gemini function declaration format
4. Define parameters with types and descriptions
5. Include required vs optional parameters
6. Return list of tool schemas

**Deliverable**: Function returning Gemini-compatible tool schemas

### Step 3: Agent System Instructions (10 minutes)

**File**: `backend/app/agent.py`

**Tasks**:
1. Create `AGENT_INSTRUCTIONS` constant (multi-line string)
2. Define TodoBot personality and tone
3. List all capabilities (create, view, complete, delete, update)
4. Provide natural language examples for each operation
5. Include clarification guidelines
6. Add error handling instructions
7. Specify response format expectations

**Deliverable**: Comprehensive system prompt for agent behavior

### Step 4: Agent Runner Function (20 minutes)

**File**: `backend/app/agent.py`

**Tasks**:
1. Create `async run_agent()` function
2. Parameters: user_message (str), user_id (str), history (list)
3. Validate inputs (user_id is UUID, message not empty)
4. Build conversation messages from history
5. Add current user message
6. Call Gemini generate_content() with tools
7. Parse response for text and function calls
8. Execute function calls if present (call MCP tools)
9. Format response with results
10. Handle errors gracefully
11. Return response dict

**Deliverable**: Working agent runner that processes messages and executes tools

### Step 5: Tool Execution Handler (15 minutes)

**File**: `backend/app/agent.py`

**Tasks**:
1. Create `async execute_tool()` function
2. Parameters: tool_name (str), tool_args (dict), user_id (str)
3. Import and call appropriate MCP tool
4. Always pass user_id to tools
5. Catch tool execution errors
6. Return tool result or error message
7. Format result for inclusion in conversation

**Deliverable**: Tool execution wrapper with error handling

### Step 6: Response Formatting (10 minutes)

**File**: `backend/app/agent.py`

**Tasks**:
1. Create `format_agent_response()` function
2. Extract text from Gemini response
3. Extract function calls if present
4. Format tool results for user
5. Add emoji for confirmations
6. Return structured response dict

**Deliverable**: Response formatter producing user-friendly output

### Step 7: Conversation Context Helper (5 minutes)

**File**: `backend/app/agent.py`

**Tasks**:
1. Create `build_conversation_history()` function
2. Accept list of previous messages
3. Format for Gemini API (role + parts structure)
4. Limit to recent messages (e.g., last 20)
5. Include system instructions at start
6. Return formatted message list

**Deliverable**: Context formatter ensuring correct API format

### Step 8: Test Suite (20 minutes)

**File**: `backend/app/test_agent.py`

**Tasks**:
1. Create pytest async test fixtures
2. Mock Gemini API responses
3. Test each user story scenario:
   - Task creation ("Add buy groceries")
   - Task viewing ("Show my tasks")
   - Task completion ("Mark groceries done")
   - Task deletion ("Delete groceries task")
   - Task update ("Change task to...")
4. Test error scenarios:
   - Missing user_id
   - Invalid input
   - Tool execution failure
   - API failure
5. Test conversation context
6. Assert responses match expectations

**Deliverable**: Comprehensive test suite covering all scenarios

### Step 9: Documentation (10 minutes)

**Files**: README additions, docstrings

**Tasks**:
1. Add module-level docstring to agent.py
2. Add docstrings to all functions
3. Document function parameters and return types
4. Create usage examples in docstrings
5. Update backend README with agent section
6. Document environment variables

**Deliverable**: Well-documented agent module

### Step 10: Integration Validation (10 minutes)

**Manual testing**:
1. Test agent with real Gemini API
2. Verify each MCP tool executes correctly
3. Test multi-turn conversations
4. Verify user isolation works
5. Test error handling
6. Validate response quality

**Deliverable**: Working agent validated against all user stories

## Dependencies

### Internal Dependencies

- **MCP Task Server** (Feature 015): All 5 tools must be functional
  - add_task, list_tasks, complete_task, delete_task, update_task
- **Database**: PostgreSQL with tasks table (via MCP tools)
- **Environment Configuration**: python-dotenv for GEMINI_API_KEY

### External Dependencies

- **google-generativeai==0.8.3**: Already installed (from Feature 013)
- **Gemini 2.0 Flash API**: Requires valid API key and quota
- **pytest-asyncio**: For testing async functions

## Success Criteria

From specification, the implementation must achieve:

**Functional**:
- [x] Agent integrates with all 5 MCP tools
- [x] Understands natural language for create/view/complete/delete/update
- [x] Validates user_id before tool execution
- [x] Provides friendly responses with emoji
- [x] Asks for clarification when needed
- [x] Handles errors gracefully
- [x] Supports conversation history
- [x] Formats task lists with status indicators
- [x] Identifies tasks by title matching

**Non-Functional**:
- [ ] Response time P95 < 3 seconds (to be validated)
- [ ] 90% intent identification accuracy (to be measured)
- [ ] Context across 5+ conversation turns
- [ ] Zero security vulnerabilities (user isolation enforced)
- [ ] Code follows quality standards (type hints, <30 lines/function)

## Risks & Mitigation

### Risk 1: Gemini API Rate Limiting (High)

- **Impact**: Agent may fail during peak usage
- **Mitigation**:
  - Implement exponential backoff
  - Cache recent responses where appropriate
  - Provide clear error messages to users
  - Monitor API usage and set quotas

### Risk 2: Natural Language Ambiguity (Medium)

- **Impact**: Agent may misinterpret user intent
- **Mitigation**:
  - Include clarification in system prompt
  - Test with diverse phrasings
  - Allow user to undo/correct actions
  - Iterate on prompt based on feedback

### Risk 3: Tool Execution Failures (Medium)

- **Impact**: Agent calls tool but it fails (DB error, etc.)
- **Mitigation**:
  - Comprehensive error handling in execute_tool()
  - User-friendly error messages
  - Log errors for debugging
  - Graceful degradation

### Risk 4: Context Window Limits (Low)

- **Impact**: Long conversations may exceed Gemini context window
- **Mitigation**:
  - Limit history to recent 20 messages
  - Summarize old context if needed
  - Clear documentation of limits

## Open Questions

1. **Response Streaming**: Should agent support streaming responses for better UX? (Future enhancement)
2. **Tool Call Confirmation**: Should destructive operations (delete) require explicit confirmation? (Design decision in instructions)
3. **Multi-Operation Requests**: Should agent handle "Add X and also delete Y" in single message? (Future enhancement, start with single operation)
4. **Personalization**: Should agent remember user preferences? (Out of scope, agent is stateless)

---

**Status**: Ready for Phase 0 Research
**Next Command**: Begin research phase to resolve open questions, then proceed to data model design
