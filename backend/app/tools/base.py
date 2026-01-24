"""
Base Tool Interface

This module defines the universal tool contract for local tools, MCP tools,
HTTP tools, and any other tool types. All tools implement the same interface
for consistent agent interaction.

Usage:
    from app.tools.base import Tool

    class MyTool(Tool):
        name = "my_tool"
        description = "Does something useful"

        def run(self, input: dict) -> str:
            return "result"
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class Tool(ABC):
    """
    Universal tool interface for agent tool calling.

    All tools (local, MCP, HTTP, etc.) must implement this interface
    to be used by the agent system.
    """

    name: str
    description: str

    @abstractmethod
    def run(self, input: Dict[str, Any]) -> str:
        """
        Execute the tool with given input.

        Args:
            input: Dictionary containing tool parameters

        Returns:
            String result of tool execution

        Raises:
            ValueError: If input validation fails
            Exception: For other execution errors
        """
        pass
