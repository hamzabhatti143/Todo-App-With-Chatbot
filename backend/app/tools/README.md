## # Tool Architecture - Universal Interface Pattern

This directory implements a universal tool interface pattern for agent tool calling, inspired by OpenAI SDK's tool management approach.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Agent (TodoAgent)                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │               Tool Registry (ToolRegistry)                 │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐         │  │
│  │  │ AddTaskTool │ │ ListTaskTool│ │CompleteTask │   ...   │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘         │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Universal Tool Interface                      │
│                        (Tool base class)                         │
│                                                                  │
│  class Tool(ABC):                                                │
│      name: str                                                   │
│      description: str                                            │
│      def run(self, input: dict) -> str: ...                      │
└─────────────────────────────────────────────────────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           ▼                  ▼                  ▼
    ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
    │ Local Tools │   │  MCP Tools  │   │ HTTP Tools  │
    │ (task_tools)│   │  (custom)   │   │  (custom)   │
    └─────────────┘   └─────────────┘   └─────────────┘
```

## Key Components

### 1. Tool Base Interface (`base.py`)

The universal contract that ALL tools must implement:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class Tool(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, input: Dict[str, Any]) -> str:
        pass
```

**Benefits**:
- Consistent interface across all tool types
- Easy to add new tools
- Framework-agnostic design
- Works with local, MCP, HTTP, or any other tool type

### 2. Tool Implementations (`task_tools.py`)

Concrete tool implementations following the interface:

```python
from app.tools.base import Tool

class AddTaskTool(Tool):
    name = "add_task"
    description = "Adds a task. Input: {user_id: str, title: str, description: str}"

    async def run(self, input: dict) -> str:
        # Tool logic here
        user_id = input.get("user_id")
        title = input.get("title")
        description = input.get("description", "")

        result = await add_task(user_id=user_id, title=title, description=description)
        return result
```

**Implemented Tools**:
- `AddTaskTool` - Create new tasks
- `ListTasksTool` - Retrieve user tasks
- `CompleteTaskTool` - Mark tasks as completed
- `DeleteTaskTool` - Delete tasks permanently
- `UpdateTaskTool` - Modify task details

### 3. Tool Registry (`agent_refactored.py::ToolRegistry`)

Manages tool registration and lookup:

```python
class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """Register a tool in the registry."""
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        """Get tool by name."""
        return self._tools.get(name)

    def get_all(self) -> Dict[str, Tool]:
        """Get all registered tools."""
        return self._tools.copy()
```

**Benefits**:
- Centralized tool management
- Dynamic tool registration
- Easy tool lookup by name
- Supports tool introspection

### 4. Agent with Tool Execution (`agent_refactored.py::TodoAgent`)

The agent orchestrates tool calling using the registry:

```python
class TodoAgent:
    def __init__(self, config: Optional[AgentConfig] = None):
        self.tool_registry = ToolRegistry()
        self._register_tools()
        self._initialize_client()

    def _register_tools(self) -> None:
        """Register all available tools."""
        tools = [
            AddTaskTool(),
            ListTasksTool(),
            CompleteTaskTool(),
            DeleteTaskTool(),
            UpdateTaskTool()
        ]
        for tool in tools:
            self.tool_registry.register(tool)

    async def _execute_tool(self, function_call, user_id: str) -> ToolCall:
        """Execute tool using universal interface."""
        tool_name = function_call.name
        arguments = dict(function_call.args)
        arguments["user_id"] = user_id

        # Lookup tool in registry
        tool = self.tool_registry.get(tool_name)
        if not tool:
            raise ValueError(f"Unknown tool: {tool_name}")

        # Execute tool using universal interface
        result = await tool.run(arguments)

        return ToolCall(name=tool_name, arguments=arguments, result=result, success=True)
```

## Usage Examples

### Basic Usage

```python
import asyncio
from app.agent_refactored import TodoAgent, AgentRequest

async def main():
    # Initialize agent (tools auto-registered)
    agent = TodoAgent()

    # Create request
    request = AgentRequest(
        user_id="550e8400-e29b-41d4-a716-446655440000",
        message="Add buy groceries and call mom"
    )

    # Run agent
    response = await agent.run(request)

    # Display results
    print(response.message)
    for tool_call in response.tool_calls:
        print(f"Tool: {tool_call.name}, Result: {tool_call.result}")

asyncio.run(main())
```

### Adding Custom Tools

```python
from app.tools.base import Tool
import requests

class WeatherTool(Tool):
    name = "get_weather"
    description = "Get weather for a location. Input: {location: str}"

    async def run(self, input: dict) -> str:
        location = input.get("location")
        # Fetch weather from API
        response = requests.get(f"https://api.weather.com/{location}")
        return response.text

# Register with agent
agent = TodoAgent()
agent.tool_registry.register(WeatherTool())
```

### MCP Tool Integration

```python
from app.tools.base import Tool

class MCPTool(Tool):
    name = "mcp_execute"
    description = "Executes action on MCP server"

    async def run(self, input: dict) -> str:
        # Call MCP server via HTTP, STDIO, or WebSocket
        response = requests.post("http://mcp-server", json=input)
        return f"MCP response for {input}"

# Register MCP tool
agent.tool_registry.register(MCPTool())
```

## Design Principles

### 1. Universal Interface
- All tools implement the same `Tool` interface
- Consistent `run(input: dict) -> str` signature
- Works with any tool type (local, remote, MCP, HTTP)

### 2. Separation of Concerns
- **Tool Interface** (`base.py`): Defines contract
- **Tool Implementations** (`task_tools.py`): Business logic
- **Tool Registry**: Management and lookup
- **Agent**: Orchestration and execution

### 3. Extensibility
- Easy to add new tools by implementing `Tool` interface
- No changes to agent code when adding tools
- Dynamic tool registration at runtime

### 4. Type Safety
- Strong typing with Pydantic models
- Type hints throughout codebase
- Validation at tool boundaries

### 5. Async-First
- All tools are async by default
- Non-blocking I/O operations
- Proper error handling with try-catch

## Comparison with Original Structure

### Original Structure
```python
# Direct MCP tool integration
from app.mcp_server.tools import add_task, list_tasks

# Agent directly calls MCP tools
if tool_name == "add_task":
    result = await add_task(**arguments)
elif tool_name == "list_tasks":
    result = await list_tasks(**arguments)
# ... more elif branches
```

**Issues**:
- Tight coupling between agent and MCP tools
- Hard to add new tool types (HTTP, custom, etc.)
- Agent needs to know about every tool
- Difficult to test tools in isolation

### Refactored Structure
```python
# Universal tool interface
class Tool(ABC):
    def run(self, input: dict) -> str: pass

# Tool implementations
class AddTaskTool(Tool):
    async def run(self, input: dict) -> str:
        return await add_task(**input)

# Agent uses registry
tool = self.tool_registry.get(tool_name)
result = await tool.run(arguments)
```

**Benefits**:
- Loose coupling via interface
- Easy to add any tool type
- Agent is tool-agnostic
- Tools can be tested independently
- Follows SOLID principles

## Testing

### Unit Testing Tools

```python
import pytest
from app.tools.task_tools import AddTaskTool

@pytest.mark.asyncio
async def test_add_task_tool():
    tool = AddTaskTool()

    input_data = {
        "user_id": "test-user-id",
        "title": "Test Task",
        "description": "Test Description"
    }

    result = await tool.run(input_data)

    assert "Test Task" in result
    assert tool.name == "add_task"
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_agent_with_tools():
    agent = TodoAgent()

    request = AgentRequest(
        user_id="test-user-id",
        message="Add buy groceries"
    )

    response = await agent.run(request)

    assert response.message
    assert len(response.tool_calls) > 0
    assert response.tool_calls[0].name == "add_task"
```

## Performance Considerations

### Tool Execution
- Tools run async for non-blocking I/O
- Tool registry uses dict lookup (O(1))
- Minimal overhead from interface abstraction

### Scaling
- Tool instances are lightweight
- Registry can handle 100+ tools
- Async execution allows concurrent tool calls

## Security

### Input Validation
- All tools validate input parameters
- User ID enforcement at tool boundary
- Type validation via Pydantic

### Error Handling
- Tools catch and return structured errors
- No exception propagation to agent
- User-friendly error messages

## Migration Guide

### From Old Agent to New Agent

1. **Import new agent**:
```python
# Old
from app.agent import TodoBot

# New
from app.agent_refactored import TodoAgent
```

2. **Same interface** (backward compatible):
```python
# Works the same
agent = TodoAgent()
response = await agent.run(request)
```

3. **Tool customization** (optional):
```python
# New: Add custom tools
agent = TodoAgent()
agent.tool_registry.register(MyCustomTool())
```

## Future Enhancements

### Planned Features
- [ ] Tool schema introspection
- [ ] Tool versioning
- [ ] Tool middleware (logging, caching, rate limiting)
- [ ] Tool composition (chain multiple tools)
- [ ] Tool marketplace/plugin system
- [ ] Streaming tool responses

### Extension Points
- Add `Tool.schema()` method for automatic Gemini schema generation
- Implement `ToolMiddleware` for cross-cutting concerns
- Add `ToolChain` for multi-step tool workflows
- Support `ToolPlugin` for dynamic loading

## References

- **OpenAI SDK Tool Pattern**: Similar tool interface and registry approach
- **MCP Protocol**: Model Context Protocol for external tool servers
- **SOLID Principles**: Followed throughout the architecture

## Support

For questions or issues with the tool architecture:
- Check `example_agent_usage.py` for usage examples
- Review `base.py` for interface definition
- See `task_tools.py` for implementation patterns

---

**Version**: 1.0.0
**Last Updated**: 2026-01-23
**Status**: Production Ready
