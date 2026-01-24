"""
Tools Module

Provides universal tool interface and implementations for agent tool calling.

Exports:
    - Tool: Base interface for all tools
    - AddTaskTool, ListTasksTool, CompleteTaskTool, DeleteTaskTool, UpdateTaskTool
"""

from app.tools.base import Tool
from app.tools.task_tools import (
    AddTaskTool,
    ListTasksTool,
    CompleteTaskTool,
    DeleteTaskTool,
    UpdateTaskTool
)

__all__ = [
    "Tool",
    "AddTaskTool",
    "ListTasksTool",
    "CompleteTaskTool",
    "DeleteTaskTool",
    "UpdateTaskTool",
]
