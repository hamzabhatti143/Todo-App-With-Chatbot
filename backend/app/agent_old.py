"""
TodoBot: Gemini AI Agent for Task Management

This module implements a conversational AI agent that enables natural language
task management through integration with MCP Task Server tools.

Usage:
    from app.agent import TodoBot, AgentRequest, AgentResponse

    agent = TodoBot()
    request = AgentRequest(
        user_id="550e8400-e29b-41d4-a716-446655440000",
        message="Add buy groceries"
    )
    response = await agent.run(request)
"""

import logging
from typing import List, Dict, Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator
import google.generativeai as genai

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
# Configuration Models
# ============================================================================

class AgentConfig(BaseModel):
    """Configuration for TodoBot agent initialization."""

    model_name: str = Field(
        default="gemini-2.0-flash",  # Changed from -exp to stable version
        description="Gemini model identifier"
    )
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_output_tokens: int = Field(default=2048, gt=0, le=8192)
    max_conversation_messages: int = Field(default=20, gt=0)
    timeout_seconds: int = Field(default=30, gt=0)


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
    arguments: Dict[str, Any]
    result: str
    success: bool


class AgentResponse(BaseModel):
    """Response from TodoBot agent."""

    message: str
    tool_calls: List[ToolCall] = Field(default_factory=list)
    error: Optional[str] = None


# ============================================================================
# System Instructions
# ============================================================================

SYSTEM_INSTRUCTIONS = """You are TodoBot, a friendly AI assistant for task management.

**Your Capabilities**:
You have 5 tools: add_task, list_tasks, complete_task, delete_task, update_task

**Guidelines**:

1. **Creating Tasks** (add_task):
   - Extract clear, concise titles from user input
   - Use description for additional details
   - Confirm with ✅ emoji

2. **Viewing Tasks** (list_tasks):
   - Default to "all" status
   - Use "pending" or "completed" when user specifies
   - Present clearly with ◯ (pending) and ✓ (completed)

3. **Completing Tasks** (complete_task):
   - If user references by title, call list_tasks first to find task_id
   - Match titles fuzzy and case-insensitive
   - Ask for clarification if multiple matches
   - Confirm with ✓ emoji

4. **Deleting Tasks** (delete_task):
   - Same pattern as completing: list first if needed
   - Confirm deletion

5. **Updating Tasks** (update_task):
   - Same pattern: list first if referenced by title
   - Confirm update with new details

**Task Identification Rules**:
When user references task by title (not UUID):
1. Call list_tasks to get all user tasks
2. Match reference to titles (fuzzy, case-insensitive)
3. Single match: use that task_id
4. Multiple matches: ask which one
5. No match: inform user

**Style**:
- Friendly and concise
- Use emojis sparingly (✅ ◯ ✓)
- Ask clarifying questions when unclear
- No technical jargon in errors

**Important**:
- Only access tasks for the authenticated user_id
- Never invent task IDs - always call list_tasks first
- Always confirm successful operations
"""


# ============================================================================
# MCP Tool Declarations (Gemini Format)
# ============================================================================

def _create_mcp_tools():
    """Create MCP tool declarations in Gemini format."""
    return genai.protos.Tool(
        function_declarations=[
            genai.protos.FunctionDeclaration(
                name='add_task',
                description=(
                    'Create a new task. Use when user wants to add, create, or '
                    'remember something. Examples: "add buy groceries", '
                    '"create task to call mom"'
                ),
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        'user_id': genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description='UUID of user (from context)'
                        ),
                        'title': genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description='Task title (1-200 chars)'
                        ),
                        'description': genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description='Optional description (max 1000 chars)'
                        )
                    },
                    required=['user_id', 'title']
                )
            ),
            genai.protos.FunctionDeclaration(
                name='list_tasks',
                description=(
                    'Get user\'s tasks with optional filter. Use when user wants '
                    'to see, show, list tasks. Examples: "show my tasks", '
                    '"what\'s pending"'
                ),
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        'user_id': genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description='UUID of user'
                        ),
                        'status': genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description='Filter: "all", "pending", or "completed"'
                        )
                    },
                    required=['user_id']
                )
            ),
            genai.protos.FunctionDeclaration(
                name='complete_task',
                description=(
                    'Mark task as done. Use when user wants to complete, finish '
                    'a task. If user references by title, call list_tasks first '
                    'to find task_id.'
                ),
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        'user_id': genai.protos.Schema(
                            type=genai.protos.Type.STRING
                        ),
                        'task_id': genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description='UUID of task'
                        )
                    },
                    required=['user_id', 'task_id']
                )
            ),
            genai.protos.FunctionDeclaration(
                name='delete_task',
                description=(
                    'Remove task permanently. Use when user wants to delete, '
                    'remove, cancel. If referenced by title, call list_tasks first.'
                ),
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        'user_id': genai.protos.Schema(type=genai.protos.Type.STRING),
                        'task_id': genai.protos.Schema(type=genai.protos.Type.STRING)
                    },
                    required=['user_id', 'task_id']
                )
            ),
            genai.protos.FunctionDeclaration(
                name='update_task',
                description=(
                    'Modify task title/description. Use when user wants to '
                    'update, change, edit, rename. If referenced by title, '
                    'call list_tasks first.'
                ),
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        'user_id': genai.protos.Schema(type=genai.protos.Type.STRING),
                        'task_id': genai.protos.Schema(type=genai.protos.Type.STRING),
                        'title': genai.protos.Schema(type=genai.protos.Type.STRING),
                        'description': genai.protos.Schema(type=genai.protos.Type.STRING)
                    },
                    required=['user_id', 'task_id']
                )
            )
        ]
    )


# ============================================================================
# Error Messages
# ============================================================================

ERROR_MESSAGES = {
    "rate_limit": "⚠️ Too many requests. Please try again in a moment.",
    "api_unavailable": "⚠️ AI service unavailable. Try again later.",
    "api_timeout": "⚠️ Request timed out. Please try again.",
    "api_error": "⚠️ Error processing request. Try again.",
    "task_not_found": "❌ Couldn't find task '{reference}'.",
    "permission_denied": "🔒 Permission denied.",
    "validation_error": "❌ Invalid input: {details}",
    "database_error": "⚠️ Database error. Try again.",
    "empty_input": "🤔 Please provide more details.",
    "unclear_intent": (
        "🤔 Not sure what to do. Try:\n"
        "• Add a task\n• List tasks\n• Complete a task\n"
        "• Delete a task\n• Update a task"
    ),
}


# ============================================================================
# TodoBot Agent
# ============================================================================

class TodoBot:
    """
    Conversational AI agent for natural language task management.

    Integrates with MCP Task Server tools to provide friendly
    interface for creating, viewing, completing, deleting, and
    updating tasks.
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """
        Initialize TodoBot agent.

        Args:
            config: Optional agent configuration
        """
        # Use settings from config.py if no config provided
        if config is None:
            config = AgentConfig(
                model_name=settings.gemini_model,
                temperature=settings.gemini_temperature,
                max_output_tokens=settings.gemini_max_tokens,
                timeout_seconds=settings.gemini_timeout,
            )
        self.config = config
        self.client: Optional[genai.GenerativeModel] = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        """Initialize Gemini client with tools."""
        try:
            genai.configure(api_key=settings.gemini_api_key)

            generation_config = {
                "temperature": self.config.temperature,
                "max_output_tokens": self.config.max_output_tokens,
            }

            self.client = genai.GenerativeModel(
                model_name=self.config.model_name,
                generation_config=generation_config,
                tools=_create_mcp_tools(),
                system_instruction=SYSTEM_INSTRUCTIONS
            )

            logger.info(
                f"TodoBot initialized: {self.config.model_name}"
            )

        except Exception as e:
            logger.error(f"Failed to initialize TodoBot: {e}")
            raise

    async def run(self, request: AgentRequest) -> AgentResponse:
        """
        Process user message and execute tool calls.

        Args:
            request: Agent request with user message and context

        Returns:
            Agent response with message and tool calls
        """
        if not self.client:
            raise ValueError("TodoBot client not initialized")

        try:
            # Prepare conversation history
            history = self._prepare_history(
                request.conversation_history
            )

            # Start chat session
            chat = self.client.start_chat(history=history)

            # Send message
            response = chat.send_message(request.message)

            # Process response
            tool_calls = []
            response_text = ""

            # Check for function calls
            if hasattr(response, "parts"):
                for part in response.parts:
                    if hasattr(part, "function_call"):
                        # Execute tool call
                        tool_result = await self._execute_tool(
                            part.function_call,
                            request.user_id
                        )
                        tool_calls.append(tool_result)

                        # Send tool result back to chat
                        response = chat.send_message(
                            genai.protos.Content(
                                parts=[
                                    genai.protos.Part(
                                        function_response=genai.protos.FunctionResponse(
                                            name=tool_result.name,
                                            response={
                                                "result": tool_result.result
                                            }
                                        )
                                    )
                                ]
                            )
                        )

            # Extract final text response
            if hasattr(response, "text"):
                response_text = response.text
            else:
                response_text = ERROR_MESSAGES["unclear_intent"]

            return AgentResponse(
                message=response_text,
                tool_calls=tool_calls,
                error=None
            )

        except Exception as e:
            logger.error(f"Error in TodoBot.run: {e}")
            return AgentResponse(
                message=ERROR_MESSAGES["api_error"],
                tool_calls=[],
                error=str(e)
            )

    def _prepare_history(
        self,
        messages: Optional[List[ConversationMessage]]
    ) -> List[Dict[str, Any]]:
        """
        Convert conversation history to Gemini format.

        Args:
            messages: List of conversation messages

        Returns:
            Gemini-formatted history (last N messages)
        """
        if not messages:
            return []

        # Take last N messages
        max_msgs = self.config.max_conversation_messages
        recent = messages[-max_msgs:] if len(messages) > max_msgs else messages

        # Convert to Gemini format
        history = []
        for msg in recent:
            role = "user" if msg.role == "user" else "model"
            history.append({
                "role": role,
                "parts": [msg.content]
            })

        return history

    async def _execute_tool(
        self,
        function_call,
        user_id: str
    ) -> ToolCall:
        """
        Execute MCP tool and return result.

        Args:
            function_call: Gemini function call object
            user_id: Authenticated user ID

        Returns:
            Tool call result
        """
        tool_name = function_call.name
        arguments = dict(function_call.args)

        # Ensure user_id is set
        arguments["user_id"] = user_id

        logger.info(f"Executing tool: {tool_name} with {arguments}")

        try:
            # Route to appropriate MCP tool
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

            return ToolCall(
                name=tool_name,
                arguments=arguments,
                result=result,
                success=True
            )

        except ValueError as e:
            # Tool validation or permission errors
            error_msg = str(e)
            logger.warning(f"Tool {tool_name} error: {error_msg}")

            return ToolCall(
                name=tool_name,
                arguments=arguments,
                result=error_msg,
                success=False
            )

        except Exception as e:
            # Unexpected errors
            error_msg = ERROR_MESSAGES["database_error"]
            logger.error(f"Unexpected error in {tool_name}: {e}")

            return ToolCall(
                name=tool_name,
                arguments=arguments,
                result=error_msg,
                success=False
            )
