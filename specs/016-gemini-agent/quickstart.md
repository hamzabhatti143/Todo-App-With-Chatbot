# Quick Start Guide: Gemini AI Agent

**Branch**: `016-gemini-agent` | **Date**: 2026-01-17

## Overview

This guide shows how to use the TodoBot agent for natural language task management.

---

## Installation

### Prerequisites

- Python 3.11+
- google-generativeai==0.8.3 (already installed)
- Existing MCP Task Server (Feature 015)
- Gemini API key

### Setup

1. **Set Gemini API Key**:
```bash
# Add to backend/.env
GEMINI_API_KEY=your-api-key-here
```

2. **No Additional Dependencies**:
The agent uses existing dependencies from Feature 013 and Feature 015.

---

## Basic Usage

### Simple Example

```python
from app.agent import TodoBot, AgentRequest, AgentResponse

# Initialize agent
agent = TodoBot()

# Create request
request = AgentRequest(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    message="Add buy groceries"
)

# Run agent
response: AgentResponse = await agent.run(request)

print(response.message)
# Output: ✅ Task created: Buy groceries (ID: 7c9e6679-...)
```

---

## Usage Examples

### Example 1: Create a Task

**User Input**:
```python
request = AgentRequest(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    message="Add buy groceries tomorrow"
)

response = await agent.run(request)
```

**Agent Response**:
```
✅ Task created: Buy groceries (ID: 7c9e6679-7425-40de-944b-e07fc1f90ae7)
```

**Tool Calls**:
```python
response.tool_calls[0].name  # "add_task"
response.tool_calls[0].arguments  # {"user_id": "...", "title": "Buy groceries", "description": "Tomorrow"}
response.tool_calls[0].success  # True
```

---

### Example 2: List Tasks

**User Input**:
```python
request = AgentRequest(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    message="Show my tasks"
)

response = await agent.run(request)
```

**Agent Response**:
```
Your tasks:
◯ Buy groceries
◯ Call mom
✓ Finish report
```

**Tool Calls**:
```python
response.tool_calls[0].name  # "list_tasks"
response.tool_calls[0].arguments  # {"user_id": "...", "status": "all"}
```

---

### Example 3: Complete a Task

**User Input**:
```python
request = AgentRequest(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    message="Mark the groceries task as done"
)

response = await agent.run(request)
```

**Agent Response**:
```
✓ Completed: Buy groceries
```

**Tool Calls** (2 calls - list first, then complete):
```python
response.tool_calls[0].name  # "list_tasks"
response.tool_calls[1].name  # "complete_task"
response.tool_calls[1].arguments  # {"user_id": "...", "task_id": "7c9e6679-..."}
```

---

### Example 4: Delete a Task

**User Input**:
```python
request = AgentRequest(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    message="Delete the shopping task"
)

response = await agent.run(request)
```

**Agent Response**:
```
✅ Deleted: Shopping
```

---

### Example 5: Update a Task

**User Input**:
```python
request = AgentRequest(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    message="Change the title of the groceries task to 'Buy groceries and fruits'"
)

response = await agent.run(request)
```

**Agent Response**:
```
✅ Updated task: Buy groceries and fruits
```

---

## Conversation Context

### Multi-Turn Conversation

```python
# Turn 1: Create task
request1 = AgentRequest(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    message="Add buy groceries"
)
response1 = await agent.run(request1)

# Turn 2: View tasks (with context)
request2 = AgentRequest(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    message="Show my tasks",
    conversation_history=[
        {"role": "user", "content": "Add buy groceries"},
        {"role": "assistant", "content": response1.message}
    ]
)
response2 = await agent.run(request2)

# Turn 3: Complete task (with context)
request3 = AgentRequest(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    message="Mark that task as done",  # "that task" refers to recent context
    conversation_history=[
        {"role": "user", "content": "Add buy groceries"},
        {"role": "assistant", "content": response1.message},
        {"role": "user", "content": "Show my tasks"},
        {"role": "assistant", "content": response2.message}
    ]
)
response3 = await agent.run(request3)
```

**Note**: Conversation history is maintained by the caller (e.g., chat API endpoint), not the agent.

---

## Advanced Usage

### Custom Configuration

```python
from app.agent import TodoBot, AgentConfig

# Create custom config
config = AgentConfig(
    model_name="gemini-2.0-flash-exp",
    temperature=0.5,  # More deterministic
    max_output_tokens=1024,  # Shorter responses
    max_conversation_messages=10,  # Shorter context
    timeout_seconds=15,  # Faster timeout
    max_retries=5  # More retries
)

# Initialize agent with custom config
agent = TodoBot(config=config)
```

---

### Error Handling

```python
from app.agent import TodoBot, AgentRequest, AgentResponse

agent = TodoBot()

try:
    request = AgentRequest(
        user_id="550e8400-e29b-41d4-a716-446655440000",
        message="Add a task"
    )

    response = await agent.run(request)

    if response.error:
        print(f"Error: {response.error}")
    else:
        print(f"Success: {response.message}")

except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

### Checking Tool Calls

```python
response = await agent.run(request)

print(f"Number of tool calls: {len(response.tool_calls)}")

for tool_call in response.tool_calls:
    print(f"Tool: {tool_call.name}")
    print(f"Arguments: {tool_call.arguments}")
    print(f"Success: {tool_call.success}")
    print(f"Result: {tool_call.result}")
```

---

## Integration with REST API

### Example: Chat Endpoint

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.agent import TodoBot, AgentRequest, AgentResponse
from app.database import get_session
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter()
agent = TodoBot()

@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(
    message: str,
    conversation_history: List[dict] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Send a message to the TodoBot agent."""

    try:
        # Create agent request
        request = AgentRequest(
            user_id=str(current_user.id),
            message=message,
            conversation_history=conversation_history
        )

        # Run agent
        response = await agent.run(request)

        # Return response
        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
```

---

## Natural Language Examples

### Task Creation

| User Says | Agent Calls | Result |
|-----------|-------------|--------|
| "Add buy groceries" | add_task(title="Buy groceries") | Task created |
| "Create a task to call mom tomorrow" | add_task(title="Call mom", description="Tomorrow") | Task created |
| "Remind me to exercise" | add_task(title="Exercise") | Task created |
| "Add finish report by Friday with high priority" | add_task(title="Finish report", description="By Friday with high priority") | Task created |

### Task Viewing

| User Says | Agent Calls | Result |
|-----------|-------------|--------|
| "Show my tasks" | list_tasks(status="all") | All tasks |
| "What's pending?" | list_tasks(status="pending") | Pending tasks only |
| "List completed tasks" | list_tasks(status="completed") | Completed tasks only |
| "What do I need to do?" | list_tasks(status="pending") | Pending tasks |

### Task Completion

| User Says | Agent Calls | Result |
|-----------|-------------|--------|
| "Mark the groceries task as done" | list_tasks → complete_task | Task completed |
| "Complete task 3" | list_tasks → complete_task | Task completed |
| "Finish the report task" | list_tasks → complete_task | Task completed |
| "I'm done with the shopping task" | list_tasks → complete_task | Task completed |

### Task Deletion

| User Says | Agent Calls | Result |
|-----------|-------------|--------|
| "Delete the shopping task" | list_tasks → delete_task | Task deleted |
| "Remove task 2" | list_tasks → delete_task | Task deleted |
| "Cancel the meeting task" | list_tasks → delete_task | Task deleted |

### Task Updates

| User Says | Agent Calls | Result |
|-----------|-------------|--------|
| "Change the groceries task title to 'Buy groceries and fruits'" | list_tasks → update_task | Title updated |
| "Update the description of the report task" | list_tasks → update_task | Description updated |
| "Rename the shopping task to 'Weekly shopping'" | list_tasks → update_task | Title updated |

---

## Edge Cases

### Ambiguous Task Reference

**User Input**: "Complete the task"

**Agent Response**:
```
🤔 I found multiple pending tasks:
1. Buy groceries
2. Call mom
3. Finish report

Which one would you like to complete?
```

### No Matching Task

**User Input**: "Delete the meeting task"

**Agent Response**:
```
❌ I couldn't find a task matching 'meeting task'. Could you be more specific?
```

### Multiple Matches

**User Input**: "Complete the report task"

**Agent Response** (if 2 tasks have "report" in title):
```
🤔 I found multiple tasks matching 'report task':
1. Finish report
2. Review quarterly report

Which one did you mean?
```

### Empty or Unclear Input

**User Input**: "Do something"

**Agent Response**:
```
🤔 I'm not sure what you'd like me to do. Try asking me to:
• Add a task
• List tasks
• Complete a task
• Delete a task
• Update a task
```

---

## Testing

### Unit Tests

```python
import pytest
from app.agent import TodoBot, AgentRequest

@pytest.mark.asyncio
async def test_create_task():
    """Test creating a task through agent."""
    agent = TodoBot()

    request = AgentRequest(
        user_id="550e8400-e29b-41d4-a716-446655440000",
        message="Add test task"
    )

    response = await agent.run(request)

    assert response.error is None
    assert "Task created" in response.message
    assert len(response.tool_calls) == 1
    assert response.tool_calls[0].name == "add_task"
    assert response.tool_calls[0].success is True
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_conversation_flow():
    """Test multi-turn conversation."""
    agent = TodoBot()
    user_id = "550e8400-e29b-41d4-a716-446655440000"

    # Turn 1: Create task
    req1 = AgentRequest(user_id=user_id, message="Add buy groceries")
    res1 = await agent.run(req1)
    assert res1.error is None

    # Turn 2: View tasks
    req2 = AgentRequest(
        user_id=user_id,
        message="Show my tasks",
        conversation_history=[
            {"role": "user", "content": "Add buy groceries"},
            {"role": "assistant", "content": res1.message}
        ]
    )
    res2 = await agent.run(req2)
    assert res2.error is None
    assert "Buy groceries" in res2.message

    # Turn 3: Complete task
    req3 = AgentRequest(
        user_id=user_id,
        message="Mark the groceries task as done",
        conversation_history=[
            {"role": "user", "content": "Add buy groceries"},
            {"role": "assistant", "content": res1.message},
            {"role": "user", "content": "Show my tasks"},
            {"role": "assistant", "content": res2.message}
        ]
    )
    res3 = await agent.run(req3)
    assert res3.error is None
    assert "Completed" in res3.message
```

---

## Performance Considerations

### Response Time

- Typical response: 1-3 seconds
- With tool calls: 2-5 seconds (depends on number of tools)
- With disambiguation: 2-4 seconds

### Token Usage

- Average request: ~500-1000 tokens (including conversation history)
- Average response: ~100-300 tokens
- Tool calls add ~200-500 tokens each

### Rate Limiting

- Gemini API: Varies by tier (check Google Cloud console)
- Recommended: Implement rate limiting at API endpoint level
- Existing implementation: 10 requests/minute per user (Feature 013)

---

## Troubleshooting

### "Gemini client not initialized"

**Cause**: Missing or invalid GEMINI_API_KEY

**Solution**:
```bash
# Check .env file
cat backend/.env | grep GEMINI_API_KEY

# Set if missing
echo "GEMINI_API_KEY=your-key-here" >> backend/.env
```

### "Tool execution failed"

**Cause**: MCP tool error (database, validation, etc.)

**Solution**: Check tool error message in `response.tool_calls[].result`

### "Conversation history too long"

**Cause**: More than 20 messages in conversation_history

**Solution**: Trim to last 20 messages before calling agent

---

## Best Practices

### 1. Always Provide user_id

```python
# ✅ Good - user_id from authenticated session
request = AgentRequest(
    user_id=str(current_user.id),  # From JWT token
    message=user_message
)

# ❌ Bad - hardcoded or missing user_id
request = AgentRequest(
    user_id="00000000-0000-0000-0000-000000000000",
    message=user_message
)
```

### 2. Maintain Conversation History

```python
# ✅ Good - provide recent context
request = AgentRequest(
    user_id=user_id,
    message=new_message,
    conversation_history=recent_messages[-20:]  # Last 20 messages
)

# ❌ Bad - no context
request = AgentRequest(
    user_id=user_id,
    message=new_message
)
```

### 3. Handle Errors Gracefully

```python
# ✅ Good - check for errors
response = await agent.run(request)
if response.error:
    logger.error(f"Agent error: {response.error}")
    return {"message": "Sorry, I encountered an error."}

# ❌ Bad - ignore errors
response = await agent.run(request)
return {"message": response.message}  # Might be error message
```

### 4. Log Tool Calls

```python
# ✅ Good - log for debugging
response = await agent.run(request)
for tool_call in response.tool_calls:
    logger.info(f"Tool: {tool_call.name}, Success: {tool_call.success}")

# ❌ Bad - no logging
response = await agent.run(request)
```

---

## API Reference

See `data-model.md` for complete API documentation:
- AgentConfig
- AgentRequest
- AgentResponse
- ToolCall
- ConversationMessage

---

## Next Steps

After implementing the agent:

1. **Add to Chat API**: Integrate agent into existing chat endpoint (Feature 013)
2. **Add Rate Limiting**: Protect agent endpoint from abuse
3. **Add Conversation Storage**: Store agent conversations in database
4. **Add Analytics**: Track tool call success rates, response times
5. **Add UI**: Create chat interface in frontend

---

## Resources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [MCP Tools Documentation](../015-mcp-task-server/TOOLS.md)
- [Feature Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Data Model](./data-model.md)

---

**Status**: Quick start guide complete ✅
**Next Phase**: Phase 2 - Implementation
