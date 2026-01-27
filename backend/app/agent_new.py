"""
TodoBot: AI Agent for Task Management using OpenAI Agents SDK

This module implements a conversational AI agent using the OpenAI Agents SDK
with GPT models for natural language task management.

Usage:
    from app.agent_new import TodoBot, AgentRequest, AgentResponse

    agent = TodoBot()
    request = AgentRequest(
        user_id="550e8400-e29b-41d4-a716-446655440000",
        message="Add buy groceries"
    )
    response = await agent.run(request)
"""

import logging
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, validator
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled

from app.config import settings
from app.mcp_server.tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task
)

logger = logging.getLogger(__name__)


# ============================================================================
# Request/Response Models
# ============================================================================

class ConversationMessage(BaseModel):
    """A single message in the conversation."""

    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., min_length=1)

    @validator("role")
    def validate_role(cls, v):
        if v not in ["user", "assistant"]:
            raise ValueError("Role must be 'user' or 'assistant'")
        return v


class AgentRequest(BaseModel):
    """Request to the TodoBot agent."""

    user_id: str = Field(..., description="UUID of authenticated user")
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_history: Optional[List[ConversationMessage]] = None

    @validator("user_id")
    def validate_user_id(cls, v):
        try:
            UUID(v)
        except ValueError:
            raise ValueError("user_id must be valid UUID")
        return v

    @validator("message")
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError("Message cannot be empty")
        return v.strip()


class ToolCall(BaseModel):
    """Tool call executed by agent."""

    name: str
    arguments: dict
    result: str
    success: bool


class AgentResponse(BaseModel):
    """Response from TodoBot agent."""

    message: str
    tool_calls: List[ToolCall] = Field(default_factory=list)
    error: Optional[str] = None


# ============================================================================
# Tool Definitions with @function_tool Decorator
# ============================================================================

@function_tool
async def tool_add_task(user_id: str, title: str, description: str = "") -> str:
    """
    Create a new task for the user.

    Args:
        user_id: UUID of the authenticated user
        title: Task title (1-200 characters)
        description: Optional task description (max 1000 characters)

    Returns:
        Success message with task details
    """
    try:
        result = await add_task(user_id=user_id, title=title, description=description)
        return result
    except Exception as e:
        logger.error(f"Error in tool_add_task: {e}")
        return f"Failed to create task: {str(e)}"


@function_tool
async def tool_list_tasks(user_id: str, status: str = "all") -> str:
    """
    Get the user's tasks with optional status filter.

    Args:
        user_id: UUID of the authenticated user
        status: Filter tasks by status - "all", "pending", or "completed"

    Returns:
        Formatted list of tasks
    """
    try:
        result = await list_tasks(user_id=user_id, status=status)
        return result
    except Exception as e:
        logger.error(f"Error in tool_list_tasks: {e}")
        return f"Failed to list tasks: {str(e)}"


@function_tool
async def tool_complete_task(user_id: str, task_id: str) -> str:
    """
    Mark a task as completed.

    Args:
        user_id: UUID of the authenticated user
        task_id: UUID of the task to complete

    Returns:
        Success message
    """
    try:
        result = await complete_task(user_id=user_id, task_id=task_id)
        return result
    except Exception as e:
        logger.error(f"Error in tool_complete_task: {e}")
        return f"Failed to complete task: {str(e)}"


@function_tool
async def tool_delete_task(user_id: str, task_id: str) -> str:
    """
    Delete a task permanently.

    Args:
        user_id: UUID of the authenticated user
        task_id: UUID of the task to delete

    Returns:
        Success message
    """
    try:
        result = await delete_task(user_id=user_id, task_id=task_id)
        return result
    except Exception as e:
        logger.error(f"Error in tool_delete_task: {e}")
        return f"Failed to delete task: {str(e)}"


@function_tool
async def tool_update_task(user_id: str, task_id: str, title: str = "", description: str = "") -> str:
    """
    Update a task's title or description.

    Args:
        user_id: UUID of the authenticated user
        task_id: UUID of the task to update
        title: New title (optional)
        description: New description (optional)

    Returns:
        Success message with updated task details
    """
    try:
        result = await update_task(user_id=user_id, task_id=task_id, title=title, description=description)
        return result
    except Exception as e:
        logger.error(f"Error in tool_update_task: {e}")
        return f"Failed to update task: {str(e)}"


# ============================================================================
# System Instructions
# ============================================================================

SYSTEM_INSTRUCTIONS = """You are TodoBot, a friendly AI assistant for task management.

**Your Capabilities**:
You have 5 tools to help users manage their tasks:
- tool_add_task: Create new tasks
- tool_list_tasks: View tasks (all, pending, or completed)
- tool_complete_task: Mark tasks as done
- tool_delete_task: Remove tasks
- tool_update_task: Modify task details

**Guidelines**:

1. **Creating Tasks** (tool_add_task):
   - Extract clear, concise titles from user input
   - Use description for additional details
   - Confirm creation

2. **Viewing Tasks** (tool_list_tasks):
   - Default to "all" status
   - Use "pending" or "completed" when user specifies

3. **Completing Tasks** (tool_complete_task):
   - If user references by title, call tool_list_tasks first to find task_id
   - Match titles fuzzy and case-insensitive
   - Ask for clarification if multiple matches
   - Confirm completion

4. **Deleting Tasks** (tool_delete_task):
   - Same pattern as completing: list first if needed
   - Confirm deletion

5. **Updating Tasks** (tool_update_task):
   - Same pattern: list first if referenced by title
   - Confirm update with new details

**Task Identification Rules**:
When user references task by title (not UUID):
1. Call tool_list_tasks to get all user tasks
2. Match reference to titles (fuzzy, case-insensitive)
3. Single match: use that task_id
4. Multiple matches: ask which one
5. No match: inform user

**Style**:
- Friendly and concise
- Ask clarifying questions when unclear
- No technical jargon in errors

**Important**:
- All tools require user_id parameter - this is automatically provided
- Only access tasks for the authenticated user_id
- Never invent task IDs - always call tool_list_tasks first
- Always confirm successful operations
"""


# ============================================================================
# TodoBot Agent
# ============================================================================

class TodoBot:
    """
    Conversational AI agent for natural language task management.

    Uses OpenAI Agents SDK with GPT models for understanding and
    responding to natural language task management requests.
    """

    def __init__(self):
        """Initialize TodoBot agent with OpenAI Agents SDK."""
        self.agent = None
        self._initialize_agent()

    def _initialize_agent(self) -> None:
        """Initialize the agent with OpenAI model and tools."""
        try:
            # Disable tracing to avoid SDK interference
            set_tracing_disabled(True)

            # Verify API key is loaded
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY not configured in environment")

            logger.info(f"OPENAI_API_KEY loaded: {settings.openai_api_key[:20]}...")

            # Initialize AsyncOpenAI with OpenAI base URL
            provider = AsyncOpenAI(
                api_key=settings.openai_api_key,
                base_url="https://api.openai.com/v1"
            )

            # Configure model using OpenAIChatCompletionsModel
            model = OpenAIChatCompletionsModel(
                model=settings.openai_model,
                openai_client=provider
            )

            # Create agent with @function_tool decorated tools
            self.agent = Agent(
                name="TodoBot",
                instructions=SYSTEM_INSTRUCTIONS,
                model=model,
                tools=[
                    tool_add_task,
                    tool_list_tasks,
                    tool_complete_task,
                    tool_delete_task,
                    tool_update_task
                ]
            )

            logger.info(f"TodoBot agent initialized with model: {settings.openai_model}")

        except Exception as e:
            logger.error(f"Failed to initialize TodoBot: {e}")
            raise

    async def run(self, request: AgentRequest) -> AgentResponse:
        """
        Process user message and execute tool calls through Runner.run().

        Args:
            request: Agent request with user message and context

        Returns:
            Agent response with message and tool calls
        """
        if not self.agent:
            raise ValueError("TodoBot agent not initialized")

        try:
            # Prepare context with user_id for all tool calls
            context = {"user_id": request.user_id}

            # Execute agent through Runner.run()
            result = await Runner.run(self.agent, request.message, context=context)

            # Extract response from result.final_output
            response_text = result.final_output if hasattr(result, 'final_output') else "No response generated"

            # Extract tool calls if available
            tool_calls = []
            # TODO: Parse tool calls from result if needed for response metadata

            logger.info(f"TodoBot executed successfully for user {request.user_id}")

            return AgentResponse(
                message=response_text,
                tool_calls=tool_calls,
                error=None
            )

        except Exception as e:
            logger.error(f"Error in TodoBot.run: {e}")
            return AgentResponse(
                message="Error processing request. Please try again.",
                tool_calls=[],
                error=str(e)
            )
