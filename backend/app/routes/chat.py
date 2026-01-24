"""Chat API routes for conversational task management."""

import logging
import time
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from sqlalchemy.exc import OperationalError, DBAPIError

from app.database import get_session
from app.dependencies import get_current_user
from app.models.user import User
from app.models.message import MessageRole
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse
from app.services.conversation_service import ConversationService
from app.agent import TodoBot, AgentRequest, ConversationMessage
from app.middleware.rate_limit import chat_rate_limit, limiter

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat", response_model=ChatMessageResponse)
@limiter.limit("10/minute")  # Rate limiting: 10 requests per minute per user
async def send_chat_message(
    request: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Send a chat message and receive AI agent response.

    The AI agent (TodoBot) interprets the message, performs task operations via MCP tools,
    and returns a conversational response.

    Args:
        request: ChatMessageRequest with message content and optional conversation_id
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        ChatMessageResponse with AI response and task data

    Raises:
        HTTPException: 400 for invalid requests, 500 for server errors
    """
    # Capture start time for performance monitoring
    start_time = time.time()

    try:
        # Step 1: Get or create conversation
        if request.conversation_id:
            conversation = ConversationService.get_conversation(
                conversation_id=request.conversation_id,
                user_id=current_user.id,
                session=session,
            )

            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Conversation {request.conversation_id} not found",
                )
        else:
            # Create new conversation
            conversation = ConversationService.create_conversation(
                user_id=current_user.id,
                session=session,
            )

        # Step 2: Save user message to database
        user_message = ConversationService.save_message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=request.content,
            session=session,
        )

        logger.info(f"Saved user message {user_message.id} in conversation {conversation.id}")

        # Step 3: Get conversation history for context
        conversation_history = ConversationService.get_conversation_history(
            conversation_id=conversation.id,
            user_id=current_user.id,
            session=session,
            limit=20,  # Last 20 messages for context
        )

        # Convert to TodoBot ConversationMessage format (exclude the just-saved user message)
        history_for_agent = [
            ConversationMessage(
                role="user" if msg.role == MessageRole.USER else "assistant",
                content=msg.content,
            )
            for msg in conversation_history[:-1]  # Exclude last message (current one)
        ]

        # Step 4: Initialize TodoBot agent
        agent = TodoBot()

        # Step 5: Create agent request
        agent_request = AgentRequest(
            user_id=str(current_user.id),
            message=request.content,
            conversation_history=history_for_agent if history_for_agent else None,
        )

        # Step 6: Run agent and get response
        try:
            agent_response = await agent.run(agent_request)

            response_text = agent_response.message
            tool_calls = agent_response.tool_calls

            # Collect task data from successful add_task calls
            task_data = None
            for tool_call in tool_calls:
                if tool_call.name == "add_task" and tool_call.success:
                    if not task_data:
                        task_data = {"tasks": []}
                    # Parse task from result string
                    # The result format is "Task created: [title] (ID: [uuid])"
                    task_data["tasks"].append({
                        "result": tool_call.result
                    })

        except Exception as agent_error:
            logger.error(f"TodoBot agent error: {agent_error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI agent unavailable. Please try again later.",
            )

        # Step 7: Save assistant response to database
        assistant_message = ConversationService.save_message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=response_text,
            session=session,
        )

        logger.info(f"Saved assistant message {assistant_message.id}")

        # Step 8: Log request duration and return response
        duration = time.time() - start_time
        logger.info(
            f"Chat request completed in {duration:.2f}s "
            f"(conversation_id={conversation.id}, user_id={current_user.id})"
        )

        # Check performance threshold (SC-001: <5 seconds p95)
        if duration > 5.0:
            logger.warning(
                f"Chat request exceeded 5s threshold: {duration:.2f}s "
                f"(conversation_id={conversation.id})"
            )

        return ChatMessageResponse(
            conversation_id=conversation.id,
            message_id=assistant_message.id,
            role="assistant",
            content=response_text,
            created_at=assistant_message.created_at,
            task_data=task_data,
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except ValueError as ve:
        # Handle validation errors
        logger.error(f"Validation error: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve),
        )

    except (OperationalError, DBAPIError) as db_error:
        # Handle database connection/operational errors
        logger.error(f"Database error in chat endpoint: {db_error}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is temporarily unavailable. Please try again later.",
        )

    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred processing your message. Please try again.",
        )
