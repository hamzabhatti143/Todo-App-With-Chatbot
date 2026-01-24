"""MCP Tool Registry for managing AI agent tools."""

import logging
from typing import Dict, Any, Callable, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class MCPTool:
    """Data class representing an MCP tool."""

    name: str
    description: str
    function: Callable
    parameters: Dict[str, Any]


class MCPToolRegistry:
    """Registry for managing MCP tools available to the AI agent."""

    def __init__(self):
        """Initialize the tool registry."""
        self._tools: Dict[str, MCPTool] = {}
        logger.info("MCP Tool Registry initialized")

    def register_tool(
        self,
        name: str,
        description: str,
        function: Callable,
        parameters: Dict[str, Any],
    ) -> None:
        """
        Register a new MCP tool in the registry.

        Args:
            name: Unique name for the tool
            description: Human-readable description of what the tool does
            function: The callable function to execute when tool is invoked
            parameters: JSON schema describing the tool's parameters

        Raises:
            ValueError: If tool name already exists
        """
        if name in self._tools:
            raise ValueError(f"Tool '{name}' is already registered")

        tool = MCPTool(
            name=name,
            description=description,
            function=function,
            parameters=parameters,
        )

        self._tools[name] = tool
        logger.info(f"Registered tool: {name}")

    def get_tool(self, name: str) -> Optional[MCPTool]:
        """
        Get a tool by name.

        Args:
            name: Name of the tool to retrieve

        Returns:
            MCPTool object if found, None otherwise
        """
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        """
        Get list of all registered tool names.

        Returns:
            List of tool names
        """
        return list(self._tools.keys())

    def get_all_tools(self) -> Dict[str, MCPTool]:
        """
        Get all registered tools.

        Returns:
            Dictionary of tool name to MCPTool objects
        """
        return self._tools.copy()

    def execute_tool(self, name: str, **kwargs) -> Any:
        """
        Execute a registered tool with given arguments.

        Args:
            name: Name of the tool to execute
            **kwargs: Arguments to pass to the tool function

        Returns:
            Result of the tool execution

        Raises:
            ValueError: If tool not found
            Exception: If tool execution fails
        """
        tool = self.get_tool(name)

        if not tool:
            raise ValueError(f"Tool '{name}' not found in registry")

        try:
            logger.info(f"Executing tool: {name} with args: {kwargs}")
            result = tool.function(**kwargs)
            logger.info(f"Tool '{name}' executed successfully")
            return result

        except Exception as e:
            logger.error(f"Error executing tool '{name}': {e}")
            raise

    def get_tools_for_gemini(self) -> List[Dict[str, Any]]:
        """
        Get tools in Gemini API format for tool calling.

        Returns:
            List of tool definitions in Gemini format
        """
        gemini_tools = []

        for tool in self._tools.values():
            gemini_tools.append(
                {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                }
            )

        return gemini_tools

    def unregister_tool(self, name: str) -> bool:
        """
        Unregister a tool from the registry.

        Args:
            name: Name of the tool to unregister

        Returns:
            True if tool was unregistered, False if not found
        """
        if name in self._tools:
            del self._tools[name]
            logger.info(f"Unregistered tool: {name}")
            return True

        return False


# Global registry instance
tool_registry = MCPToolRegistry()
