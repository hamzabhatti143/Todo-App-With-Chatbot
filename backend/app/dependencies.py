"""
FastAPI Dependencies

Reusable dependencies for authentication and database sessions.
"""

import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from uuid import UUID
from jose import JWTError

from app.database import get_session
from app.auth import decode_token
from app.models.user import User

logger = logging.getLogger(__name__)
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    Get the current authenticated user from JWT token.

    Args:
        credentials: HTTP Bearer credentials containing JWT token
        session: Database session

    Returns:
        User: The authenticated user

    Raises:
        HTTPException: If credentials are invalid
    """
    logger.info("Authentication: Extracting user from JWT token")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        logger.info(f"Authentication: Token received (length: {len(token)})")

        payload = decode_token(token)
        username: str = payload.get("sub")

        if username is None:
            logger.error("Authentication: No 'sub' claim found in token")
            raise credentials_exception

        logger.info(f"Authentication: Extracted username from token: {username}")

    except JWTError as e:
        logger.error(f"Authentication: JWT decode error: {e}")
        raise credentials_exception

    # Get user from database by username
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()

    if user is None:
        logger.error(f"Authentication: User '{username}' not found in database")
        raise credentials_exception

    logger.info(f"Authentication: Successfully authenticated user {user.username} ({user.email})")
    return user


async def get_current_user_id(
    current_user: User = Depends(get_current_user)
) -> UUID:
    """
    Get the current user's ID.

    Args:
        current_user: The authenticated user

    Returns:
        UUID: The user's ID
    """
    return current_user.id


async def get_current_username(
    current_user: User = Depends(get_current_user)
) -> str:
    """
    Get the current user's username.

    Args:
        current_user: The authenticated user

    Returns:
        str: The user's username
    """
    return current_user.username
