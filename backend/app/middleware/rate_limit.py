"""Rate limiting middleware for API endpoints."""

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from jose import jwt, JWTError

from app.config import settings


def get_user_id_or_ip(request: Request) -> str:
    """
    Extract user ID from JWT token for rate limiting, fallback to IP address.

    This enables user-based rate limiting instead of IP-based, which prevents
    issues with:
    - Multiple users behind same NAT/proxy
    - Single user with multiple IPs

    Args:
        request: FastAPI request object

    Returns:
        User ID from JWT token if authenticated, otherwise IP address
    """
    try:
        # Try to extract JWT token from Authorization header
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")

            # Decode token to get user_id
            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm]
            )
            user_id = payload.get("sub")

            if user_id:
                return f"user:{user_id}"

    except (JWTError, KeyError, AttributeError):
        # Token invalid or missing, fall back to IP
        pass

    # Fallback to IP address for unauthenticated requests
    return f"ip:{get_remote_address(request)}"


# Initialize rate limiter with user-based key function
limiter = Limiter(
    key_func=get_user_id_or_ip,  # User-based rate limiting
    default_limits=["100/minute"],  # Default global limit
    storage_uri=settings.redis_url if settings.redis_url else "memory://",
)


def get_rate_limit_exceeded_handler():
    """Get custom rate limit exceeded handler."""

    async def custom_rate_limit_exceeded_handler(
        request: Request, exc: RateLimitExceeded
    ):
        """
        Custom handler for rate limit exceeded errors.

        Args:
            request: FastAPI request object
            exc: RateLimitExceeded exception

        Returns:
            JSON response with error details
        """
        return {
            "error": "Rate limit exceeded",
            "detail": f"You have exceeded the rate limit. Please try again later.",
            "retry_after": exc.detail if hasattr(exc, "detail") else None,
        }

    return custom_rate_limit_exceeded_handler


# Rate limit decorators for specific endpoints

def chat_rate_limit():
    """Rate limiter for chat endpoints."""
    return limiter.limit(settings.rate_limit_chat)


def agent_rate_limit():
    """Rate limiter for AI agent endpoints."""
    return limiter.limit(settings.rate_limit_agent)


# Export limiter and handlers
__all__ = [
    "limiter",
    "get_rate_limit_exceeded_handler",
    "chat_rate_limit",
    "agent_rate_limit",
]
