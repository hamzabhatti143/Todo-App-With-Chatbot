"""
Task Management Tools

Local tools implementing the Tool interface for task management operations.
These tools wrap the MCP server functionality with the universal Tool contract.

Usage:
    from app.tools.task_tools import AddTaskTool

    tool = AddTaskTool()
    result = tool.run({"user_id": "uuid", "title": "Buy groceries"})
"""

from typing import Dict, Any
import json

from app.tools.base import Tool
from app.mcp_server.tools import (
    add_task as mcp_add_task,
    list_tasks as mcp_list_tasks,
    complete_task as mcp_complete_task,
    delete_task as mcp_delete_task,
    update_task as mcp_update_task
)


class AddTaskTool(Tool):
    """
    Tool for creating new tasks.

    Input: {user_id: str, title: str, description: str (optional)}
    Output: JSON string with task details
    """

    name = "add_task"
    description = (
        "Create a new task. Use when user wants to add, create, or "
        "remember something. Input: {user_id: str, title: str, description: str}"
    )

    async def run(self, input: Dict[str, Any]) -> str:
        """
        Create a new task for the user.

        Args:
            input: Dictionary with user_id, title, and optional description

        Returns:
            JSON string with task details or error message
        """
        try:
            user_id = input.get("user_id")
            title = input.get("title")
            description = input.get("description", "")

            if not user_id or not title:
                return json.dumps({
                    "error": "Missing required fields: user_id and title"
                })

            result = await mcp_add_task(
                user_id=user_id,
                title=title,
                description=description
            )

            return result

        except Exception as e:
            return json.dumps({"error": str(e)})


class ListTasksTool(Tool):
    """
    Tool for retrieving user's tasks.

    Input: {user_id: str, status: str (optional: "all", "pending", "completed")}
    Output: JSON string with task list
    """

    name = "list_tasks"
    description = (
        "Get user's tasks with optional filter. Use when user wants "
        "to see, show, list tasks. Input: {user_id: str, status: str}"
    )

    async def run(self, input: Dict[str, Any]) -> str:
        """
        Retrieve tasks for the user with optional status filter.

        Args:
            input: Dictionary with user_id and optional status filter

        Returns:
            JSON string with task list or error message
        """
        try:
            user_id = input.get("user_id")
            status = input.get("status", "all")

            if not user_id:
                return json.dumps({"error": "Missing required field: user_id"})

            result = await mcp_list_tasks(user_id=user_id, status=status)

            return result

        except Exception as e:
            return json.dumps({"error": str(e)})


class CompleteTaskTool(Tool):
    """
    Tool for marking tasks as completed.

    Input: {user_id: str, task_id: str}
    Output: JSON string with updated task details
    """

    name = "complete_task"
    description = (
        "Mark task as done. Use when user wants to complete, finish "
        "a task. If user references by title, call list_tasks first "
        "to find task_id. Input: {user_id: str, task_id: str}"
    )

    async def run(self, input: Dict[str, Any]) -> str:
        """
        Mark a task as completed.

        Args:
            input: Dictionary with user_id and task_id

        Returns:
            JSON string with updated task details or error message
        """
        try:
            user_id = input.get("user_id")
            task_id = input.get("task_id")

            if not user_id or not task_id:
                return json.dumps({
                    "error": "Missing required fields: user_id and task_id"
                })

            result = await mcp_complete_task(user_id=user_id, task_id=task_id)

            return result

        except Exception as e:
            return json.dumps({"error": str(e)})


class DeleteTaskTool(Tool):
    """
    Tool for deleting tasks permanently.

    Input: {user_id: str, task_id: str}
    Output: JSON string with deletion confirmation
    """

    name = "delete_task"
    description = (
        "Remove task permanently. Use when user wants to delete, "
        "remove, cancel. If referenced by title, call list_tasks first. "
        "Input: {user_id: str, task_id: str}"
    )

    async def run(self, input: Dict[str, Any]) -> str:
        """
        Delete a task permanently.

        Args:
            input: Dictionary with user_id and task_id

        Returns:
            JSON string with deletion confirmation or error message
        """
        try:
            user_id = input.get("user_id")
            task_id = input.get("task_id")

            if not user_id or not task_id:
                return json.dumps({
                    "error": "Missing required fields: user_id and task_id"
                })

            result = await mcp_delete_task(user_id=user_id, task_id=task_id)

            return result

        except Exception as e:
            return json.dumps({"error": str(e)})


class UpdateTaskTool(Tool):
    """
    Tool for updating task details.

    Input: {user_id: str, task_id: str, title: str (optional), description: str (optional)}
    Output: JSON string with updated task details
    """

    name = "update_task"
    description = (
        "Modify task title/description. Use when user wants to "
        "update, change, edit, rename. If referenced by title, "
        "call list_tasks first. Input: {user_id: str, task_id: str, "
        "title: str, description: str}"
    )

    async def run(self, input: Dict[str, Any]) -> str:
        """
        Update task title and/or description.

        Args:
            input: Dictionary with user_id, task_id, and optional title/description

        Returns:
            JSON string with updated task details or error message
        """
        try:
            user_id = input.get("user_id")
            task_id = input.get("task_id")
            title = input.get("title")
            description = input.get("description")

            if not user_id or not task_id:
                return json.dumps({
                    "error": "Missing required fields: user_id and task_id"
                })

            result = await mcp_update_task(
                user_id=user_id,
                task_id=task_id,
                title=title,
                description=description
            )

            return result

        except Exception as e:
            return json.dumps({"error": str(e)})
