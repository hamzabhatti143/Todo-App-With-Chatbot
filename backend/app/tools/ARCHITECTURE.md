# Tool Architecture - Visual Guide

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              CLIENT REQUEST                              │
│                   "Add buy groceries and call mom"                       │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           FASTAPI ENDPOINT                               │
│                         POST /api/chat                                   │
│                                                                           │
│  async def chat(request: ChatRequest):                                   │
│      agent = TodoAgent()  # Initialize agent                             │
│      response = await agent.run(agent_request)                           │
│      return response                                                     │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           TODOAGENT (Agent)                              │
│                                                                           │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │                    TOOL REGISTRY                                │    │
│  │                                                                  │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐           │    │
│  │  │ AddTaskTool  │ │ ListTaskTool │ │CompleteTask  │  ...      │    │
│  │  │   .run()     │ │   .run()     │ │   .run()     │           │    │
│  │  └──────────────┘ └──────────────┘ └──────────────┘           │    │
│  │                                                                  │    │
│  │  register(tool) ──► Stores tool by name                        │    │
│  │  get(name) ──► Returns tool instance                           │    │
│  │  to_gemini_tools() ──► Converts to Gemini format              │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                           │
│  Step 1: Send message to Gemini ────────────────────┐                   │
│                                                      │                   │
│  Step 2: Gemini responds with tool calls ◄──────────┘                   │
│                                                      │                   │
│  Step 3: Execute tools via registry.get(name) ──────┤                   │
│                                                      │                   │
│  Step 4: Send results back to Gemini ───────────────┘                   │
│                                                      │                   │
│  Step 5: Gemini generates final response ◄──────────┘                   │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           GOOGLE GEMINI 2.0 FLASH                        │
│                                                                           │
│  Input: User message + Available tools                                   │
│  Output: Tool calls (function_call) OR Text response                     │
│                                                                           │
│  Example tool call:                                                      │
│  {                                                                        │
│    "name": "add_task",                                                   │
│    "arguments": {                                                        │
│      "user_id": "uuid",                                                  │
│      "title": "Buy groceries"                                            │
│    }                                                                     │
│  }                                                                       │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         TOOL INTERFACE (Universal)                       │
│                                                                           │
│  class Tool(ABC):                                                        │
│      name: str                        ◄─── Tool identifier               │
│      description: str                 ◄─── What the tool does            │
│      async def run(input: dict) -> str  ◄─── Execute tool logic         │
│                                                                           │
│  Benefits:                                                               │
│  ✓ All tools follow same contract                                       │
│  ✓ Easy to add new tools                                                │
│  ✓ Agent is tool-agnostic                                               │
│  ✓ Tools can be tested independently                                    │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    TOOL IMPLEMENTATIONS                                  │
│                                                                           │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌──────────────────┐│
│  │   LOCAL TOOLS       │  │    MCP TOOLS        │  │   HTTP TOOLS     ││
│  │   (task_tools.py)   │  │   (custom)          │  │   (custom)       ││
│  │                     │  │                     │  │                  ││
│  │ AddTaskTool         │  │ MCPTool             │  │ WeatherTool      ││
│  │ ListTaskTool        │  │   .run() calls      │  │   .run() calls   ││
│  │ CompleteTaskTool    │  │   MCP server via    │  │   external API   ││
│  │ DeleteTaskTool      │  │   HTTP/STDIO/       │  │   via requests   ││
│  │ UpdateTaskTool      │  │   WebSocket         │  │                  ││
│  │                     │  │                     │  │                  ││
│  │ .run() calls        │  │                     │  │                  ││
│  │ MCP server tools    │  │                     │  │                  ││
│  └─────────────────────┘  └─────────────────────┘  └──────────────────┘│
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         MCP SERVER TOOLS                                 │
│                      (mcp_server/tools.py)                               │
│                                                                           │
│  async def add_task(user_id: str, title: str, ...) -> str               │
│  async def list_tasks(user_id: str, status: str) -> str                 │
│  async def complete_task(user_id: str, task_id: str) -> str             │
│  async def delete_task(user_id: str, task_id: str) -> str               │
│  async def update_task(user_id: str, task_id: str, ...) -> str          │
│                                                                           │
│  These interact with:                                                    │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        DATABASE (PostgreSQL)                             │
│                                                                           │
│  Tasks Table:                                                            │
│  - id (UUID)                                                             │
│  - user_id (UUID, FK)                                                    │
│  - title (VARCHAR)                                                       │
│  - description (TEXT)                                                    │
│  - completed (BOOLEAN)                                                   │
│  - created_at (TIMESTAMP)                                                │
│  - updated_at (TIMESTAMP)                                                │
└─────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Example

### Example: "Add buy groceries"

```
1. CLIENT REQUEST
   ├─► POST /api/chat
   └─► Body: { "user_id": "uuid", "message": "Add buy groceries" }

2. FASTAPI ENDPOINT
   ├─► Creates AgentRequest
   ├─► Initializes TodoAgent
   └─► Calls agent.run(request)

3. TODOAGENT
   ├─► Sends message to Gemini with available tools
   ├─► Gemini responds: "Call add_task with title='Buy groceries'"
   ├─► Agent looks up tool: registry.get("add_task")
   ├─► Tool found: AddTaskTool instance
   ├─► Executes: await tool.run({"user_id": "uuid", "title": "Buy groceries"})
   └─► Tool returns: JSON with task details

4. ADDTASKTOOL.run()
   ├─► Extracts user_id, title from input
   ├─► Validates input
   ├─► Calls: await add_task(user_id, title)
   └─► Returns: JSON string result

5. MCP add_task()
   ├─► Connects to database
   ├─► Creates Task record
   ├─► Commits transaction
   └─► Returns: "✅ Added task: Buy groceries [UUID: xxx]"

6. TODOAGENT (continued)
   ├─► Receives tool result
   ├─► Sends result back to Gemini
   ├─► Gemini generates friendly response:
   │   "✅ I've added 'Buy groceries' to your tasks!"
   └─► Returns AgentResponse to endpoint

7. FASTAPI ENDPOINT
   ├─► Converts AgentResponse to ChatResponse
   └─► Returns to client

8. CLIENT
   └─► Displays: "✅ I've added 'Buy groceries' to your tasks!"
```

## Tool Execution Flow

```
┌────────────────────────────────────────────────────────────────┐
│                    Agent.run(request)                          │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────┐
│  Step 1: Prepare conversation history                          │
│  - Convert messages to Gemini format                           │
│  - Take last N messages for context                            │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────┐
│  Step 2: Send to Gemini                                        │
│  chat.send_message(user_message)                               │
│  - Includes: message + available tools + system instructions   │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────┐
│  Step 3: Gemini Response                                       │
│  ┌──────────────────────┐                                      │
│  │ Has function_call?   │                                      │
│  └──────┬───────────────┘                                      │
│         │                                                       │
│    YES  │  NO                                                   │
│    ┌────▼────┐  ┌──────────────┐                              │
│    │ Execute │  │ Return text  │                              │
│    │ Tools   │  │ response     │                              │
│    └────┬────┘  └──────────────┘                              │
│         │                                                       │
│         ▼                                                       │
│  ┌────────────────────────────────────────────┐               │
│  │ For each function_call in response:        │               │
│  │                                             │               │
│  │ 1. Extract: name, arguments                │               │
│  │ 2. Lookup: tool = registry.get(name)       │               │
│  │ 3. Add user_id to arguments                │               │
│  │ 4. Execute: result = await tool.run(args)  │               │
│  │ 5. Collect: ToolCall(name, args, result)   │               │
│  └────────────┬────────────────────────────────┘               │
│               │                                                 │
│               ▼                                                 │
│  ┌────────────────────────────────────────────┐               │
│  │ Send tool results back to Gemini           │               │
│  │ chat.send_message(function_response)       │               │
│  └────────────┬────────────────────────────────┘               │
│               │                                                 │
│               ▼                                                 │
│  ┌────────────────────────────────────────────┐               │
│  │ Gemini generates final text response       │               │
│  │ using tool results                         │               │
│  └────────────┬────────────────────────────────┘               │
└───────────────┼─────────────────────────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────────────────────────┐
│  Step 4: Return AgentResponse                                  │
│  - message: str (final response text)                          │
│  - tool_calls: List[ToolCall] (executed tools)                 │
│  - error: Optional[str] (if any errors)                        │
└────────────────────────────────────────────────────────────────┘
```

## Tool Registry Pattern

```
┌────────────────────────────────────────────────────────────────┐
│                         ToolRegistry                            │
│                                                                  │
│  _tools: Dict[str, Tool] = {                                    │
│      "add_task": AddTaskTool(),                                 │
│      "list_tasks": ListTaskTool(),                              │
│      "complete_task": CompleteTaskTool(),                       │
│      "delete_task": DeleteTaskTool(),                           │
│      "update_task": UpdateTaskTool()                            │
│  }                                                              │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  register(tool: Tool)                                     │  │
│  │  ├─► Validates tool has name and description             │  │
│  │  ├─► Adds to _tools dict: _tools[tool.name] = tool       │  │
│  │  └─► Logs registration                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  get(name: str) -> Optional[Tool]                        │  │
│  │  ├─► Looks up tool by name                               │  │
│  │  ├─► Returns tool instance if found                      │  │
│  │  └─► Returns None if not found                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  to_gemini_tools() -> genai.protos.Tool                  │  │
│  │  ├─► Iterates over all tools                             │  │
│  │  ├─► Converts each to FunctionDeclaration                │  │
│  │  └─► Returns Gemini Tool object                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Benefits:                                                      │
│  ✓ O(1) tool lookup by name                                    │
│  ✓ Dynamic tool registration                                   │
│  ✓ Easy to add/remove tools at runtime                         │
│  ✓ Centralized tool management                                 │
└────────────────────────────────────────────────────────────────┘
```

## Adding a Custom Tool

```
┌────────────────────────────────────────────────────────────────┐
│  Step 1: Implement Tool Interface                              │
│                                                                  │
│  from app.tools.base import Tool                               │
│                                                                  │
│  class WeatherTool(Tool):                                       │
│      name = "get_weather"                                       │
│      description = "Get weather. Input: {location: str}"       │
│                                                                  │
│      async def run(self, input: dict) -> str:                  │
│          location = input.get("location")                       │
│          # Call weather API                                     │
│          response = requests.get(f"api.weather.com/{location}")│
│          return response.text                                   │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────┐
│  Step 2: Register Tool with Agent                              │
│                                                                  │
│  agent = TodoAgent()                                            │
│  agent.tool_registry.register(WeatherTool())                   │
│                                                                  │
│  # Tool is now available for Gemini to call                    │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────┐
│  Step 3: Use in Conversation                                   │
│                                                                  │
│  request = AgentRequest(                                        │
│      user_id="uuid",                                            │
│      message="What's the weather in London?"                   │
│  )                                                              │
│                                                                  │
│  response = await agent.run(request)                           │
│  # Gemini will call get_weather tool automatically             │
└────────────────────────────────────────────────────────────────┘
```

## Comparison: Before vs After

### Before (If-Elif Chain)

```python
async def _execute_tool(self, function_call, user_id):
    tool_name = function_call.name
    arguments = dict(function_call.args)

    if tool_name == "add_task":
        result = await add_task(**arguments)
    elif tool_name == "list_tasks":
        result = await list_tasks(**arguments)
    elif tool_name == "complete_task":
        result = await complete_task(**arguments)
    elif tool_name == "delete_task":
        result = await delete_task(**arguments)
    elif tool_name == "update_task":
        result = await update_task(**arguments)
    else:
        raise ValueError(f"Unknown tool: {tool_name}")

    return ToolCall(...)
```

**Issues**:
- ❌ Must modify agent code to add new tools
- ❌ Tight coupling with specific tool implementations
- ❌ Hard to support multiple tool types (MCP, HTTP, etc.)
- ❌ Tools cannot be tested independently
- ❌ No central tool management

### After (Registry Pattern)

```python
async def _execute_tool(self, function_call, user_id):
    tool_name = function_call.name
    arguments = dict(function_call.args)
    arguments["user_id"] = user_id

    # Lookup tool in registry
    tool = self.tool_registry.get(tool_name)
    if not tool:
        raise ValueError(f"Unknown tool: {tool_name}")

    # Execute via universal interface
    result = await tool.run(arguments)

    return ToolCall(...)
```

**Benefits**:
- ✅ No agent code changes to add tools
- ✅ Loose coupling via interface
- ✅ Supports any tool type (local, MCP, HTTP, custom)
- ✅ Tools can be tested independently
- ✅ Centralized tool management via registry

## Summary

The refactored architecture provides:

1. **Universal Interface**: All tools implement the same `Tool` contract
2. **Registry Pattern**: Centralized tool management with O(1) lookup
3. **Loose Coupling**: Agent doesn't know about specific tool implementations
4. **Extensibility**: Easy to add new tools without modifying agent code
5. **Testability**: Tools can be tested independently
6. **Type Safety**: Strong typing with Pydantic models
7. **Async-First**: All tools are async for non-blocking I/O

This matches the OpenAI SDK's tool management pattern and follows SOLID principles for clean, maintainable code.
