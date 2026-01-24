"""Conversation API routes for retrieving conversation history."""

import logging
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, func

from app.database import get_session
from app.dependencies import get_current_user
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.chat import (
    ConversationResponse,
    ConversationDetailResponse,
    MessageResponse,
)
from app.services.conversation_service import ConversationService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    limit: int = Query(50, ge=1, le=100, description="Maximum number of conversations to return"),
    offset: int = Query(0, ge=0, description="Number of conversations to skip"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    List all conversations for the authenticated user.

    Returns conversations ordered by most recent update first (updated_at DESC).
    Includes message count for each conversation.

    Args:
        limit: Maximum number of conversations to return (default 50, max 100)
        offset: Number of conversations to skip for pagination (default 0)
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        List of conversations with message counts
    """
    try:
        # Get conversations using the service
        conversations = ConversationService.get_user_conversations(
            user_id=current_user.id,
            session=session,
            limit=limit,
            offset=offset,
        )

        # For each conversation, count messages
        result = []
        for conversation in conversations:
            # Count messages for this conversation
            message_count_stmt = select(func.count(Message.id)).where(
                Message.conversation_id == conversation.id
            )
            message_count = session.exec(message_count_stmt).one()

            result.append(
                ConversationResponse(
                    id=conversation.id,
                    user_id=conversation.user_id,
                    created_at=conversation.created_at,
                    updated_at=conversation.updated_at,
                    message_count=message_count,
                )
            )

        logger.info(f"Retrieved {len(result)} conversations for user {current_user.id}")
        return result

    except Exception as e:
        logger.error(f"Error listing conversations: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversations",
        )


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Get a specific conversation with all its messages.

    Verifies conversation ownership before returning.
    Messages are ordered chronologically (created_at ASC).

    Args:
        conversation_id: UUID of the conversation to retrieve
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        Conversation with all messages

    Raises:
        HTTPException: 404 if conversation not found or doesn't belong to user
    """
    try:
        # Get conversation and verify ownership
        conversation = ConversationService.get_conversation(
            conversation_id=conversation_id,
            user_id=current_user.id,
            session=session,
        )

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation {conversation_id} not found",
            )

        # Get all messages for this conversation
        messages = ConversationService.get_conversation_history(
            conversation_id=conversation_id,
            user_id=current_user.id,
            session=session,
            limit=1000,  # Get all messages for detail view
        )

        # Convert to response format
        message_responses = [
            MessageResponse(
                id=msg.id,
                conversation_id=msg.conversation_id,
                role=msg.role.value,
                content=msg.content,
                created_at=msg.created_at,
            )
            for msg in messages
        ]

        logger.info(
            f"Retrieved conversation {conversation_id} with {len(message_responses)} messages"
        )

        return ConversationDetailResponse(
            id=conversation.id,
            user_id=conversation.user_id,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            messages=message_responses,
        )

    except HTTPException:
        raise
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ve),
        )
    except Exception as e:
        logger.error(f"Error retrieving conversation: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversation",
        )


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Get all messages for a specific conversation.

    Verifies conversation ownership before returning messages.
    Messages are ordered chronologically (created_at ASC).

    Args:
        conversation_id: UUID of the conversation
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        List of messages ordered by creation time

    Raises:
        HTTPException: 404 if conversation not found or doesn't belong to user
    """
    try:
        # Verify conversation exists and belongs to user
        conversation = ConversationService.get_conversation(
            conversation_id=conversation_id,
            user_id=current_user.id,
            session=session,
        )

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation {conversation_id} not found",
            )

        # Get all messages
        messages = ConversationService.get_conversation_history(
            conversation_id=conversation_id,
            user_id=current_user.id,
            session=session,
            limit=1000,  # Get all messages
        )

        # Convert to response format
        result = [
            MessageResponse(
                id=msg.id,
                conversation_id=msg.conversation_id,
                role=msg.role.value,
                content=msg.content,
                created_at=msg.created_at,
            )
            for msg in messages
        ]

        logger.info(f"Retrieved {len(result)} messages for conversation {conversation_id}")
        return result

    except HTTPException:
        raise
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ve),
        )
    except Exception as e:
        logger.error(f"Error retrieving messages: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve messages",
        )
