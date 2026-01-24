"""Service for managing conversations and messages."""

import logging
from datetime import datetime
from uuid import UUID
from typing import Optional, List
from sqlmodel import Session, select

from app.models.conversation import Conversation
from app.models.message import Message, MessageRole

logger = logging.getLogger(__name__)


class ConversationService:
    """Service class for conversation and message management."""

    @staticmethod
    def create_conversation(user_id: UUID, session: Session) -> Conversation:
        """
        Create a new conversation for a user.

        Args:
            user_id: UUID of the user
            session: Database session

        Returns:
            Created Conversation object
        """
        conversation = Conversation(
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        logger.info(f"Created conversation {conversation.id} for user {user_id}")
        return conversation

    @staticmethod
    def get_conversation(
        conversation_id: UUID,
        user_id: UUID,
        session: Session,
    ) -> Optional[Conversation]:
        """
        Get a conversation by ID with user ownership verification.

        Args:
            conversation_id: UUID of the conversation
            user_id: UUID of the user (for ownership verification)
            session: Database session

        Returns:
            Conversation object if found and owned by user, None otherwise
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )

        conversation = session.exec(statement).first()
        return conversation

    @staticmethod
    def save_message(
        conversation_id: UUID,
        role: MessageRole,
        content: str,
        session: Session,
    ) -> Message:
        """
        Save a message to a conversation.

        Args:
            conversation_id: UUID of the conversation
            role: Role of the message sender (user or assistant)
            content: Content of the message
            session: Database session

        Returns:
            Created Message object

        Raises:
            ValueError: If content is empty
        """
        if not content or len(content.strip()) == 0:
            raise ValueError("Message content cannot be empty")

        if len(content) > 5000:
            raise ValueError("Message content cannot exceed 5000 characters")

        # Create message
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content.strip(),
            created_at=datetime.utcnow(),
        )

        session.add(message)

        # Update conversation updated_at timestamp
        conversation = session.get(Conversation, conversation_id)
        if conversation:
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)

        session.commit()
        session.refresh(message)

        logger.info(
            f"Saved {role.value} message {message.id} to conversation {conversation_id}"
        )
        return message

    @staticmethod
    def get_conversation_history(
        conversation_id: UUID,
        user_id: UUID,
        session: Session,
        limit: int = 20,
    ) -> List[Message]:
        """
        Get conversation message history.

        Args:
            conversation_id: UUID of the conversation
            user_id: UUID of the user (for ownership verification)
            session: Database session
            limit: Maximum number of messages to retrieve (default 20)

        Returns:
            List of Message objects ordered by created_at ASC

        Raises:
            ValueError: If conversation not found or doesn't belong to user
        """
        # Verify conversation ownership
        conversation = ConversationService.get_conversation(
            conversation_id, user_id, session
        )

        if not conversation:
            raise ValueError(
                f"Conversation {conversation_id} not found or does not belong to user"
            )

        # Get messages ordered chronologically
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )

        messages = session.exec(statement).all()
        return list(messages)

    @staticmethod
    def get_user_conversations(
        user_id: UUID,
        session: Session,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Conversation]:
        """
        Get all conversations for a user.

        Args:
            user_id: UUID of the user
            session: Database session
            limit: Maximum number of conversations to retrieve
            offset: Number of conversations to skip

        Returns:
            List of Conversation objects ordered by updated_at DESC
        """
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
            .offset(offset)
        )

        conversations = session.exec(statement).all()
        return list(conversations)
