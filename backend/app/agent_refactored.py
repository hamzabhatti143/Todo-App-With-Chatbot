"""
TodoBot: Gemini AI Agent for Task Management (Refactored)

This module implements a conversational AI agent using Google Gemini 2.0 Flash
with a universal tool interface pattern inspired by OpenAI SDK's tool calling approach.

The refactored architecture follows these principles:
1. Universal Tool interface (Tool base class)
2. Tool registry for dynamic tool management
3. Clean separation between agent logic and tool execution
4. Async tool execution with proper error handling

Usage:
    from app.agent_refactored import TodoAgent, AgentRequest, AgentResponse

    agent = TodoAgent()
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
from app.tools import (
    Tool,
    AddTaskTool,
    ListTasksTool,
    CompleteTaskTool,
    DeleteTaskTool,
    UpdateTaskTool
)

logger = logging.getLogger(__name__)


# ============================================================================
# Configuration Models
# ============================================================================

class AgentConfig(BaseModel):
    """Configuration for TodoAgent initialization."""

    model_name: str = Field(
        default="gemini-2.0-flash-exp",
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
    """Request to the TodoAgent."""

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
    """Response from TodoAgent."""

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
# Tool Registry
# ============================================================================

class ToolRegistry:
    """
    Registry for managing agent tools.

    Provides centralized tool storage and lookup by name.
    Inspired by OpenAI SDK's tool management pattern.
    """

    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """
        Register a tool in the registry.

        Args:
            tool: Tool instance to register
        """
        self._tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def get(self, name: str) -> Optional[Tool]:
        """
        Get tool by name.

        Args:
            name: Tool name

        Returns:
            Tool instance or None if not found
        """
        return self._tools.get(name)

    def get_all(self) -> Dict[str, Tool]:
        """
        Get all registered tools.

        Returns:
            Dictionary of tool name to Tool instance
        """
        return self._tools.copy()

    def to_gemini_tools(self) -> genai.protos.Tool:
        """
        Convert registered tools to Gemini function declarations.

        Returns:
            Gemini Tool object with function declarations
        """
        function_declarations = []

        for tool in self._tools.values():
            # Create function declaration from tool
            # Note: This is a simplified conversion
            # In production, tools should provide their own schema
            function_declarations.append(
                self._create_function_declaration(tool)
            )

        return genai.protos.Tool(function_declarations=function_declarations)

    def _create_function_declaration(self, tool: Tool) -> genai.protos.FunctionDeclaration:
        """
        Create Gemini function declaration from tool.

        Args:
            tool: Tool instance

        Returns:
            Gemini FunctionDeclaration
        """
        # Define schemas for each tool
        # This should ideally come from the tool itself
        schemas = {
            "add_task": {
                "type": genai.protos.Type.OBJECT,
                "properties": {
                    "user_id": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="UUID of user"
                    ),
                    "title": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Task title (1-200 chars)"
                    ),
                    "description": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Optional description"
                    )
                },
                "required": ["user_id", "title"]
            },
            "list_tasks": {
                "type": genai.protos.Type.OBJECT,
                "properties": {
                    "user_id": genai.protos.Schema(
                        type=genai.protos.Type.STRING
                    ),
                    "status": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Filter: all, pending, completed"
                    )
                },
                "required": ["user_id"]
            },
            "complete_task": {
                "type": genai.protos.Type.OBJECT,
                "properties": {
                    "user_id": genai.protos.Schema(
                        type=genai.protos.Type.STRING
                    ),
                    "task_id": genai.protos.Schema(
                        type=genai.protos.Type.STRING
                    )
                },
                "required": ["user_id", "task_id"]
            },
            "delete_task": {
                "type": genai.protos.Type.OBJECT,
                "properties": {
                    "user_id": genai.protos.Schema(
                        type=genai.protos.Type.STRING
                    ),
                    "task_id": genai.protos.Schema(
                        type=genai.protos.Type.STRING
                    )
                },
                "required": ["user_id", "task_id"]
            },
            "update_task": {
                "type": genai.protos.Type.OBJECT,
                "properties": {
                    "user_id": genai.protos.Schema(
                        type=genai.protos.Type.STRING
                    ),
                    "task_id": genai.protos.Schema(
                        type=genai.protos.Type.STRING
                    ),
                    "title": genai.protos.Schema(
                        type=genai.protos.Type.STRING
                    ),
                    "description": genai.protos.Schema(
                        type=genai.protos.Type.STRING
                    )
                },
                "required": ["user_id", "task_id"]
            }
        }

        schema = schemas.get(tool.name, {
            "type": genai.protos.Type.OBJECT,
            "properties": {},
            "required": []
        })

        return genai.protos.FunctionDeclaration(
            name=tool.name,
            description=tool.description,
            parameters=genai.protos.Schema(**schema)
        )


# ============================================================================
# TodoAgent (Refactored)
# ============================================================================

class TodoAgent:
    """
    Conversational AI agent for natural language task management.

    Refactored architecture using:
    - Universal Tool interface
    - Tool registry pattern
    - Clean separation of concerns
    - Async tool execution
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """
        Initialize TodoAgent with tool registry.

        Args:
            config: Optional agent configuration
        """
        self.config = config or AgentConfig()
        self.tool_registry = ToolRegistry()
        self.client: Optional[genai.GenerativeModel] = None

        # Register all tools
        self._register_tools()

        # Initialize Gemini client
        self._initialize_client()

    def _register_tools(self) -> None:
        """Register all available tools in the registry."""
        tools = [
            AddTaskTool(),
            ListTasksTool(),
            CompleteTaskTool(),
            DeleteTaskTool(),
            UpdateTaskTool()
        ]

        for tool in tools:
            self.tool_registry.register(tool)

        logger.info(f"Registered {len(tools)} tools")

    def _initialize_client(self) -> None:
        """Initialize Gemini client with registered tools."""
        try:
            genai.configure(api_key=settings.gemini_api_key)

            generation_config = {
                "temperature": self.config.temperature,
                "max_output_tokens": self.config.max_output_tokens,
            }

            # Convert tools to Gemini format
            gemini_tools = self.tool_registry.to_gemini_tools()

            self.client = genai.GenerativeModel(
                model_name=self.config.model_name,
                generation_config=generation_config,
                tools=gemini_tools,
                system_instruction=SYSTEM_INSTRUCTIONS
            )

            logger.info(
                f"TodoAgent initialized: {self.config.model_name} "
                f"with {len(self.tool_registry.get_all())} tools"
            )

        except Exception as e:
            logger.error(f"Failed to initialize TodoAgent: {e}")
            raise

    async def run(self, request: AgentRequest) -> AgentResponse:
        """
        Process user message and execute tool calls.

        This method follows the OpenAI SDK pattern:
        1. Send user message to model
        2. Model responds with tool calls
        3. Execute tools using universal Tool interface
        4. Send tool results back to model
        5. Model generates final response

        Args:
            request: Agent request with user message and context

        Returns:
            Agent response with message and tool calls
        """
        if not self.client:
            raise ValueError("TodoAgent client not initialized")

        try:
            # Prepare conversation history
            history = self._prepare_history(request.conversation_history)

            # Start chat session
            chat = self.client.start_chat(history=history)

            # Send user message
            response = chat.send_message(request.message)

            # Process tool calls
            tool_calls = []
            response_text = ""

            # Check for function calls
            if hasattr(response, "parts"):
                for part in response.parts:
                    if hasattr(part, "function_call"):
                        # Execute tool using registry
                        tool_result = await self._execute_tool(
                            part.function_call,
                            request.user_id
                        )
                        tool_calls.append(tool_result)

                        # Send tool result back to model
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
                response_text = (
                    "🤔 Not sure what to do. Try adding, listing, "
                    "completing, deleting, or updating tasks."
                )

            return AgentResponse(
                message=response_text,
                tool_calls=tool_calls,
                error=None
            )

        except Exception as e:
            logger.error(f"Error in TodoAgent.run: {e}")
            return AgentResponse(
                message="⚠️ Error processing request. Try again.",
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
        Execute tool using the universal Tool interface.

        This method follows the pattern:
        1. Lookup tool by name in registry
        2. Prepare tool input (ensure user_id is set)
        3. Execute tool.run() with input
        4. Return structured result

        Args:
            function_call: Gemini function call object
            user_id: Authenticated user ID

        Returns:
            Tool call result
        """
        tool_name = function_call.name
        arguments = dict(function_call.args)

        # Ensure user_id is set for security
        arguments["user_id"] = user_id

        logger.info(f"Executing tool: {tool_name} with {arguments}")

        try:
            # Lookup tool in registry
            tool = self.tool_registry.get(tool_name)

            if not tool:
                raise ValueError(f"Unknown tool: {tool_name}")

            # Execute tool using universal interface
            result = await tool.run(arguments)

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
            error_msg = f"⚠️ Tool execution failed: {str(e)}"
            logger.error(f"Unexpected error in {tool_name}: {e}")

            return ToolCall(
                name=tool_name,
                arguments=arguments,
                result=error_msg,
                success=False
            )


# ============================================================================
# Backward Compatibility Alias
# ============================================================================

# Keep original name for backward compatibility
TodoBot = TodoAgent
