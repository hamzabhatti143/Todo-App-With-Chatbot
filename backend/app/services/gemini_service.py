"""Gemini AI service for natural language processing."""

import time
import logging
from typing import List, Dict, Any, Optional
from functools import wraps

import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

from app.config import settings

logger = logging.getLogger(__name__)


def retry_with_exponential_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
):
    """
    Decorator for exponential backoff retry logic.

    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay between retries
        exponential_base: Base for exponential calculation

    Returns:
        Decorated function with retry logic
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            num_retries = 0
            delay = initial_delay

            while True:
                try:
                    return func(*args, **kwargs)
                except (
                    google_exceptions.ResourceExhausted,
                    google_exceptions.ServiceUnavailable,
                    google_exceptions.DeadlineExceeded,
                    google_exceptions.GoogleAPICallError,
                ) as e:
                    num_retries += 1

                    if num_retries > max_retries:
                        logger.error(
                            f"Max retries ({max_retries}) exceeded for {func.__name__}: {e}"
                        )
                        raise

                    logger.warning(
                        f"Retry {num_retries}/{max_retries} for {func.__name__} after {delay}s: {e}"
                    )

                    time.sleep(delay)
                    delay = min(delay * exponential_base, max_delay)

        return wrapper

    return decorator


class GeminiService:
    """Service class for interacting with Google Gemini AI API."""

    def __init__(self):
        """Initialize Gemini service with configuration from settings."""
        self.api_key = settings.gemini_api_key
        self.model_name = settings.gemini_model
        self.temperature = settings.gemini_temperature
        self.max_tokens = settings.gemini_max_tokens
        self.timeout = settings.gemini_timeout

        self.client: Optional[genai.GenerativeModel] = None
        self.initialize_client()

    def initialize_client(self) -> None:
        """Initialize the Gemini AI client."""
        try:
            genai.configure(api_key=self.api_key)

            # Create generation config
            generation_config = {
                "temperature": self.temperature,
                "max_output_tokens": self.max_tokens,
            }

            # Initialize model
            self.client = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=generation_config,
            )

            logger.info(f"Gemini client initialized with model: {self.model_name}")

        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            raise

    @retry_with_exponential_backoff(max_retries=3, initial_delay=1.0)
    def generate_text(self, prompt: str) -> str:
        """
        Generate text from a single prompt using Gemini.

        Args:
            prompt: Input text prompt

        Returns:
            Generated text response

        Raises:
            ValueError: If client is not initialized
            google_exceptions.GoogleAPICallError: If API call fails after retries
        """
        if not self.client:
            raise ValueError("Gemini client not initialized")

        try:
            response = self.client.generate_content(prompt)
            return response.text

        except Exception as e:
            logger.error(f"Error generating text: {e}")
            raise

    @retry_with_exponential_backoff(max_retries=3, initial_delay=1.0)
    def generate_chat_response(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        system_instruction: Optional[str] = None,
    ) -> str:
        """
        Generate a chat response with conversation context.

        Args:
            message: Current user message
            conversation_history: List of previous messages with 'role' and 'content'
            system_instruction: Optional system instruction for the AI

        Returns:
            Generated chat response

        Raises:
            ValueError: If client is not initialized
            google_exceptions.GoogleAPICallError: If API call fails after retries
        """
        if not self.client:
            raise ValueError("Gemini client not initialized")

        try:
            # Build chat history in Gemini format
            chat_messages = []

            if conversation_history:
                for msg in conversation_history:
                    role = "user" if msg["role"] == "user" else "model"
                    chat_messages.append({"role": role, "parts": [msg["content"]]})

            # Add current message
            chat_messages.append({"role": "user", "parts": [message]})

            # Create chat session
            chat = self.client.start_chat(history=chat_messages[:-1])

            # Generate response
            response = chat.send_message(message)
            return response.text

        except Exception as e:
            logger.error(f"Error generating chat response: {e}")
            raise

    def generate_chat_response_with_tools(
        self,
        message: str,
        tools: List[Any],
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """
        Generate chat response with MCP tool calling capability.

        Args:
            message: Current user message
            tools: List of MCP tool definitions
            conversation_history: List of previous messages

        Returns:
            Dictionary containing response text and tool calls

        Raises:
            ValueError: If client is not initialized
        """
        if not self.client:
            raise ValueError("Gemini client not initialized")

        try:
            # Build chat history
            chat_messages = []

            if conversation_history:
                for msg in conversation_history:
                    role = "user" if msg["role"] == "user" else "model"
                    chat_messages.append({"role": role, "parts": [msg["content"]]})

            # Create model with tools
            model_with_tools = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config={
                    "temperature": self.temperature,
                    "max_output_tokens": self.max_tokens,
                },
                tools=tools,
            )

            # Create chat session
            chat = model_with_tools.start_chat(history=chat_messages)

            # Generate response
            response = chat.send_message(message)

            # Extract tool calls if any
            tool_calls = []
            if hasattr(response, "function_calls") and response.function_calls:
                for func_call in response.function_calls:
                    tool_calls.append(
                        {
                            "name": func_call.name,
                            "arguments": dict(func_call.args),
                        }
                    )

            return {
                "text": response.text if hasattr(response, "text") else "",
                "tool_calls": tool_calls,
            }

        except Exception as e:
            logger.error(f"Error generating chat response with tools: {e}")
            raise
