# Data Model: Gemini AI Agent for Task Management

**Branch**: `016-gemini-agent` | **Date**: 2026-01-17 | **Phase**: 1 - Design

## Overview

This document defines the data structures, configuration, and schemas for the TodoBot agent. The agent is stateless and uses Pydantic models for validation.

---

## Agent Configuration

### AgentConfig

Configuration for initializing the TodoBot agent.

```python
from pydantic import BaseModel, Field
from typing import Optional

class AgentConfig(BaseModel):
    """Configuration for TodoBot agent initialization."""

    model_name: str = Field(
        default="gemini-2.0-flash-exp",
        description="Gemini model identifier"
    )

    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Temperature for response generation (0.0-2.0)"
    )

    max_output_tokens: int = Field(
        default=2048,
        gt=0,
        le=8192,
        description="Maximum tokens in agent response"
    )

    max_conversation_messages: int = Field(
        default=20,
        gt=0,
        description="Maximum conversation messages to keep in context"
    )

    timeout_seconds: int = Field(
        default=30,
        gt=0,
        description="Timeout for Gemini API calls in seconds"
    )

    enable_retry: bool = Field(
        default=True,
        description="Enable exponential backoff retry for API errors"
    )

    max_retries: int = Field(
        default=3,
        ge=0,
        description="Maximum retry attempts for API errors"
    )
```

**Default Configuration**:
```python
DEFAULT_CONFIG = AgentConfig(
    model_name="gemini-2.0-flash-exp",
    temperature=0.7,
    max_output_tokens=2048,
    max_conversation_messages=20,
    timeout_seconds=30,
    enable_retry=True,
    max_retries=3
)
```

---

## Request/Response Models

### ConversationMessage

Represents a single message in the conversation history.

```python
from typing import Literal
from pydantic import BaseModel, Field

class ConversationMessage(BaseModel):
    """A single message in the conversation."""

    role: Literal["user", "assistant"] = Field(
        ...,
        description="Role of the message sender"
    )

    content: str = Field(
        ...,
        min_length=1,
        description="Message content"
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {"role": "user", "content": "Add buy groceries"},
                {"role": "assistant", "content": "Task created: Buy groceries (ID: ...)"}
            ]
        }
```

### AgentRequest

Input to the agent's `run` function.

```python
from typing import List, Optional
from pydantic import BaseModel, Field, validator

class AgentRequest(BaseModel):
    """Request to the TodoBot agent."""

    user_id: str = Field(
        ...,
        description="UUID of the authenticated user"
    )

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User's message to the agent"
    )

    conversation_history: Optional[List[ConversationMessage]] = Field(
        default=None,
        description="Previous messages in the conversation (max 20)"
    )

    @validator("user_id")
    def validate_user_id(cls, v):
        """Validate user_id is a valid UUID format."""
        from uuid import UUID
        try:
            UUID(v)
        except ValueError:
            raise ValueError("user_id must be a valid UUID")
        return v

    @validator("conversation_history")
    def validate_history_length(cls, v):
        """Ensure conversation history doesn't exceed limits."""
        if v and len(v) > 20:
            raise ValueError("conversation_history cannot exceed 20 messages")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "message": "Show my pending tasks",
                "conversation_history": [
                    {"role": "user", "content": "Add buy groceries"},
                    {"role": "assistant", "content": "Task created: Buy groceries"}
                ]
            }
        }
```

### ToolCall

Represents a tool call made by the agent.

```python
from typing import Dict, Any
from pydantic import BaseModel, Field

class ToolCall(BaseModel):
    """Represents a tool call executed by the agent."""

    name: str = Field(
        ...,
        description="Name of the MCP tool called"
    )

    arguments: Dict[str, Any] = Field(
        ...,
        description="Arguments passed to the tool"
    )

    result: str = Field(
        ...,
        description="Result returned by the tool"
    )

    success: bool = Field(
        ...,
        description="Whether the tool call succeeded"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "add_task",
                "arguments": {
                    "user_id": "550e8400-e29b-41d4-a716-446655440000",
                    "title": "Buy groceries",
                    "description": None
                },
                "result": "Task created: Buy groceries (ID: 7c9e6679-...)",
                "success": True
            }
        }
```

### AgentResponse

Output from the agent's `run` function.

```python
from typing import List, Optional
from pydantic import BaseModel, Field

class AgentResponse(BaseModel):
    """Response from the TodoBot agent."""

    message: str = Field(
        ...,
        description="Agent's response message to the user"
    )

    tool_calls: List[ToolCall] = Field(
        default_factory=list,
        description="List of tool calls executed during this turn"
    )

    error: Optional[str] = Field(
        default=None,
        description="Error message if agent encountered an error"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "✅ Task created: Buy groceries (ID: 7c9e6679-...)",
                "tool_calls": [
                    {
                        "name": "add_task",
                        "arguments": {
                            "user_id": "550e8400-...",
                            "title": "Buy groceries"
                        },
                        "result": "Task created: Buy groceries (ID: ...)",
                        "success": True
                    }
                ],
                "error": None
            }
        }
```

---

## MCP Tool Declarations

### Tool Definition Schema

Format for defining MCP tools to Gemini.

```python
from typing import Dict, Any, List
from pydantic import BaseModel, Field

class ToolParameter(BaseModel):
    """Parameter definition for a tool."""

    type: str = Field(..., description="Parameter type (string, integer, boolean, etc.)")
    description: str = Field(..., description="Parameter description")
    enum: Optional[List[str]] = Field(None, description="Allowed values (for enum types)")

class ToolParameters(BaseModel):
    """Parameters schema for a tool."""

    type: str = Field(default="object", description="Parameters type (always object)")
    properties: Dict[str, ToolParameter] = Field(..., description="Parameter definitions")
    required: List[str] = Field(default_factory=list, description="Required parameter names")

class ToolDeclaration(BaseModel):
    """OpenAPI-style tool declaration for Gemini."""

    name: str = Field(..., description="Tool name (snake_case)")
    description: str = Field(..., description="Tool description for the agent")
    parameters: ToolParameters = Field(..., description="Tool parameter schema")
```

### MCP Tool Declarations

All 5 MCP tools defined in Gemini-compatible format:

```python
MCP_TOOLS = [
    # Tool 1: add_task
    {
        "name": "add_task",
        "description": (
            "Create a new task for the user. "
            "Use this when the user wants to add, create, or remember something. "
            "Examples: 'add buy groceries', 'create a task to call mom', 'remind me to exercise'"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "UUID of the user creating the task (provided in context)"
                },
                "title": {
                    "type": "string",
                    "description": "Task title (1-200 characters, required)"
                },
                "description": {
                    "type": "string",
                    "description": "Optional task description (max 1000 characters)"
                }
            },
            "required": ["user_id", "title"]
        }
    },

    # Tool 2: list_tasks
    {
        "name": "list_tasks",
        "description": (
            "Retrieve the user's tasks with optional filtering. "
            "Use this when the user wants to see, show, list, or view their tasks. "
            "Examples: 'show my tasks', 'what's pending', 'list completed tasks'"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "UUID of the user whose tasks to retrieve"
                },
                "status": {
                    "type": "string",
                    "description": "Filter by status: 'all' (default), 'pending', or 'completed'",
                    "enum": ["all", "pending", "completed"]
                }
            },
            "required": ["user_id"]
        }
    },

    # Tool 3: complete_task
    {
        "name": "complete_task",
        "description": (
            "Mark a task as completed. "
            "Use this when the user wants to complete, finish, or mark a task as done. "
            "Examples: 'mark the groceries task as done', 'complete task 2', 'finish that task'. "
            "If the user references a task by title, call list_tasks first to find the task_id."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "UUID of the user performing the operation"
                },
                "task_id": {
                    "type": "string",
                    "description": "UUID of the task to complete"
                }
            },
            "required": ["user_id", "task_id"]
        }
    },

    # Tool 4: delete_task
    {
        "name": "delete_task",
        "description": (
            "Remove a task permanently from the database. "
            "Use this when the user wants to delete, remove, or cancel a task. "
            "Examples: 'delete the shopping task', 'remove task 3', 'cancel that task'. "
            "If the user references a task by title, call list_tasks first to find the task_id."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "UUID of the user performing the operation"
                },
                "task_id": {
                    "type": "string",
                    "description": "UUID of the task to delete"
                }
            },
            "required": ["user_id", "task_id"]
        }
    },

    # Tool 5: update_task
    {
        "name": "update_task",
        "description": (
            "Modify a task's title and/or description. "
            "Use this when the user wants to update, change, edit, or rename a task. "
            "Examples: 'change the title to...', 'update the description', 'rename that task'. "
            "If the user references a task by title, call list_tasks first to find the task_id. "
            "At least one of title or description must be provided."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "UUID of the user updating the task"
                },
                "task_id": {
                    "type": "string",
                    "description": "UUID of the task to update"
                },
                "title": {
                    "type": "string",
                    "description": "New task title (1-200 characters, optional)"
                },
                "description": {
                    "type": "string",
                    "description": "New task description (max 1000 characters, optional)"
                }
            },
            "required": ["user_id", "task_id"]
        }
    }
]
```

---

## Agent System Instructions

### System Prompt Template

Instructions embedded in the agent to guide behavior:

```python
SYSTEM_INSTRUCTIONS = """You are TodoBot, a friendly AI assistant that helps users manage their tasks through natural conversation.

**Your Capabilities**:
You have access to 5 tools for task management:
1. add_task - Create new tasks
2. list_tasks - Retrieve tasks (all, pending, or completed)
3. complete_task - Mark tasks as done
4. delete_task - Remove tasks permanently
5. update_task - Modify task title or description

**How to Help Users**:

1. **Creating Tasks**:
   - When users say "add", "create", "remind me", extract the task title and optional description
   - Call add_task with clear, concise titles
   - Confirm task creation with an emoji: ✅

2. **Viewing Tasks**:
   - When users say "show", "list", "what", call list_tasks
   - Use status filter: "all" (default), "pending", or "completed"
   - Present tasks in a clear, readable format

3. **Completing Tasks**:
   - When users say "done", "complete", "finished", mark the task as complete
   - If user references a task by title (e.g., "the groceries task"), call list_tasks first to find the task_id
   - Use fuzzy matching to identify the right task
   - If multiple matches, ask user to clarify which task they mean
   - Confirm completion with an emoji: ✓

4. **Deleting Tasks**:
   - When users say "delete", "remove", "cancel", delete the task
   - Follow same pattern as completing: list tasks first if referenced by title
   - Confirm deletion

5. **Updating Tasks**:
   - When users say "change", "update", "rename", modify the task
   - Follow same pattern: list tasks first if referenced by title
   - Confirm update with new details

**Task Identification Rules**:
- When user provides a task reference by title (not UUID):
  1. Call list_tasks to get all user tasks
  2. Match the reference to task titles (fuzzy matching, case-insensitive)
  3. If exactly one match: use that task_id
  4. If multiple matches: ask user to clarify which task
  5. If no matches: inform user no matching task found

**Conversation Style**:
- Be friendly, helpful, and concise
- Use emojis sparingly (✅ for success, ◯ for pending tasks, ✓ for completed)
- Ask clarifying questions when intent is unclear
- Provide helpful error messages (no technical jargon)
- Maintain conversation context across turns

**Error Handling**:
- If a tool call fails, explain the error in user-friendly terms
- If you can't identify the user's intent, ask them to rephrase
- If information is missing, ask for it politely

**Important**:
- You can only access and modify tasks for the authenticated user (user_id in context)
- Never assume or invent task IDs - always call list_tasks to find them
- Always confirm successful operations
- Be concise but informative in responses
"""
```

---

## Internal Data Structures

### Tool Execution Result

Internal structure for tool execution tracking:

```python
from typing import Optional
from pydantic import BaseModel

class ToolExecutionResult(BaseModel):
    """Internal result of tool execution."""

    success: bool
    result: Optional[str] = None
    error: Optional[str] = None
    tool_name: str
    arguments: Dict[str, Any]
```

### Conversation Context

Internal structure for managing conversation state:

```python
from typing import List, Dict, Any

class ConversationContext(BaseModel):
    """Internal conversation context for agent."""

    user_id: str
    messages: List[Dict[str, str]]  # Gemini format: {role, parts}
    recent_tool_calls: List[ToolExecutionResult] = Field(default_factory=list)

    def to_gemini_format(self) -> List[Dict[str, Any]]:
        """Convert to Gemini API format."""
        return [
            {
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [msg["content"]]
            }
            for msg in self.messages
        ]

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the context."""
        self.messages.append({"role": role, "content": content})

    def trim_to_limit(self, max_messages: int = 20) -> None:
        """Keep only the most recent N messages."""
        if len(self.messages) > max_messages:
            self.messages = self.messages[-max_messages:]
```

---

## Error Message Catalog

User-friendly error messages for all error scenarios:

```python
ERROR_MESSAGES = {
    # API Errors
    "rate_limit": "⚠️ I'm receiving too many requests right now. Please try again in a moment.",
    "api_unavailable": "⚠️ The AI service is temporarily unavailable. Please try again later.",
    "api_timeout": "⚠️ The request took too long. Please try again.",
    "api_error": "⚠️ I encountered an error processing your request. Please try again.",

    # Tool Errors
    "task_not_found": "❌ I couldn't find a task matching '{reference}'. Could you be more specific?",
    "permission_denied": "🔒 You don't have permission to modify that task.",
    "validation_error": "❌ Invalid input: {details}",
    "database_error": "⚠️ I couldn't save your changes due to a database error. Please try again.",
    "title_required": "❌ Please provide a title for the task.",
    "title_too_long": "❌ Task title is too long (max 200 characters).",
    "description_too_long": "❌ Task description is too long (max 1000 characters).",

    # User Input Errors
    "empty_input": "🤔 I didn't understand that. Could you please provide more details?",
    "ambiguous_task": "🤔 I found multiple tasks matching '{reference}':\n{task_list}\n\nWhich one did you mean?",
    "missing_info": "🤔 I need more information. {what_is_missing}",

    # Agent Logic Errors
    "unclear_intent": "🤔 I'm not sure what you'd like me to do. Try asking me to:\n• Add a task\n• List tasks\n• Complete a task\n• Delete a task\n• Update a task",
    "unexpected_format": "⚠️ I received an unexpected response. Please try rephrasing your request.",
}
```

---

## Validation Rules

### Input Validation

```python
from pydantic import validator

class AgentRequest(BaseModel):
    # ... (fields defined above)

    @validator("message")
    def validate_message_not_empty(cls, v):
        """Ensure message is not just whitespace."""
        if not v or len(v.strip()) == 0:
            raise ValueError("Message cannot be empty or whitespace only")
        return v.strip()

    @validator("conversation_history")
    def validate_history_alternates(cls, v):
        """Ensure history alternates between user and assistant."""
        if not v:
            return v

        for i in range(len(v) - 1):
            if v[i].role == v[i + 1].role:
                raise ValueError("Conversation history must alternate between user and assistant")

        return v
```

---

## Data Flow Diagram

```
User Request
    ↓
[AgentRequest] → Agent.run()
    ↓
Convert to Gemini format
    ↓
[ConversationContext] → Gemini API
    ↓
Gemini processes with tools
    ↓
Response with function_calls?
    ↓
Yes → Execute MCP tools → [ToolExecutionResult]
    ↓
No → Direct text response
    ↓
Format response
    ↓
[AgentResponse] → Return to caller
```

---

## Configuration Constants

```python
# Agent defaults
DEFAULT_MODEL = "gemini-2.0-flash-exp"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2048
DEFAULT_MAX_MESSAGES = 20

# Retry configuration
DEFAULT_MAX_RETRIES = 3
DEFAULT_INITIAL_DELAY = 1.0
DEFAULT_MAX_DELAY = 60.0

# Validation limits
MAX_MESSAGE_LENGTH = 2000
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000
MAX_CONVERSATION_HISTORY = 20

# Timeouts
API_TIMEOUT_SECONDS = 30
TOOL_TIMEOUT_SECONDS = 10
```

---

## Status

**Phase 1 Progress**: Data model design complete ✅

**Next Step**: Create agent system instructions template and quickstart guide

**Files Created**:
- ✅ `data-model.md` - This file

**Files Remaining**:
- ⏳ `quickstart.md` - Usage examples and integration guide
