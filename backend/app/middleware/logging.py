"""
Logging middleware for request/response tracking and error logging
"""

import logging
import time
import json
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses

    Logs:
    - Request method, path, client IP
    - Response status code and duration
    - Request/response bodies (optional, for debugging)
    - Errors with full stack traces
    """

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        """
        Process request and log details

        Args:
            request: FastAPI request object
            call_next: Next middleware/handler in chain

        Returns:
            Response object
        """
        # Generate request ID for tracking
        request_id = str(time.time())

        # Log request
        logger.info(
            f"[{request_id}] {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else "unknown",
                "user_agent": request.headers.get("user-agent", "unknown")
            }
        )

        # Start timer
        start_time = time.time()

        try:
            # Process request
            response = await call_next(request)

            # Calculate duration
            duration = time.time() - start_time

            # Log response
            logger.info(
                f"[{request_id}] {response.status_code} - {duration:.3f}s",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "duration": duration
                }
            )

            return response

        except Exception as exc:
            # Calculate duration
            duration = time.time() - start_time

            # Log error with full details
            logger.error(
                f"[{request_id}] ERROR - {str(exc)} - {duration:.3f}s",
                extra={
                    "request_id": request_id,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                    "duration": duration,
                    "path": request.url.path,
                    "method": request.method
                },
                exc_info=True  # Include full stack trace
            )

            # Re-raise to be handled by FastAPI
            raise


def log_chat_operation(
    user_id: str,
    operation: str,
    conversation_id: str = None,
    success: bool = True,
    error: str = None,
    **kwargs
):
    """
    Log chat-specific operations for monitoring and debugging

    Args:
        user_id: ID of the user performing the operation
        operation: Type of operation (e.g., "send_message", "list_conversations")
        conversation_id: ID of the conversation (if applicable)
        success: Whether the operation succeeded
        error: Error message (if failed)
        **kwargs: Additional context to log
    """
    log_data = {
        "user_id": user_id,
        "operation": operation,
        "conversation_id": conversation_id,
        "success": success,
        **kwargs
    }

    if success:
        logger.info(
            f"Chat operation: {operation} - Success",
            extra=log_data
        )
    else:
        logger.error(
            f"Chat operation: {operation} - Failed: {error}",
            extra={**log_data, "error": error}
        )


def log_mcp_tool_execution(
    tool_name: str,
    user_id: str,
    arguments: dict,
    result: dict = None,
    error: str = None
):
    """
    Log MCP tool execution for monitoring AI agent actions

    Args:
        tool_name: Name of the MCP tool (e.g., "add_task", "list_tasks")
        user_id: ID of the user whose data is being accessed
        arguments: Arguments passed to the tool
        result: Result returned by the tool (if successful)
        error: Error message (if failed)
    """
    log_data = {
        "tool_name": tool_name,
        "user_id": user_id,
        "arguments": arguments
    }

    if error:
        logger.error(
            f"MCP tool failed: {tool_name} - {error}",
            extra={**log_data, "error": error}
        )
    else:
        logger.info(
            f"MCP tool executed: {tool_name}",
            extra={**log_data, "result_summary": _summarize_result(result)}
        )


def log_gemini_api_call(
    operation: str,
    user_id: str,
    conversation_id: str = None,
    message_count: int = None,
    response_time: float = None,
    error: str = None
):
    """
    Log Gemini AI API calls for monitoring and debugging

    Args:
        operation: Type of operation (e.g., "generate_chat_response")
        user_id: ID of the user making the request
        conversation_id: ID of the conversation (if applicable)
        message_count: Number of messages in conversation context
        response_time: API response time in seconds
        error: Error message (if failed)
    """
    log_data = {
        "operation": operation,
        "user_id": user_id,
        "conversation_id": conversation_id,
        "message_count": message_count,
        "response_time": response_time
    }

    if error:
        logger.error(
            f"Gemini API call failed: {operation} - {error}",
            extra={**log_data, "error": error}
        )
    else:
        logger.info(
            f"Gemini API call: {operation} - {response_time:.3f}s",
            extra=log_data
        )


def _summarize_result(result: any) -> str:
    """
    Create a short summary of result for logging

    Args:
        result: Result to summarize

    Returns:
        String summary
    """
    if result is None:
        return "none"

    if isinstance(result, dict):
        return f"dict with {len(result)} keys"

    if isinstance(result, list):
        return f"list with {len(result)} items"

    return str(type(result).__name__)
