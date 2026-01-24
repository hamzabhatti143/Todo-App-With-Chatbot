"""
MCP Server Package

Provides MCP tools for task management operations.

Available Tools:
- add_task: Create new task
- list_tasks: Retrieve tasks with filtering
- complete_task: Mark task as completed
- delete_task: Remove task permanently
- update_task: Modify task title and/or description
"""

from app.mcp_server.tools import mcp
from app.mcp_server.server import main

__all__ = [
    "mcp",
    "main",
]
