"""
Test Script for MCP Tools

This script tests all 5 MCP tools with success and error scenarios.
Run with: python -m app.mcp_server.test_tools
"""

import asyncio
from uuid import uuid4

from app.mcp_server.tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task
)


async def test_tools():
    """Test all MCP tools with comprehensive scenarios."""

    print("🧪 Testing MCP Tools\n")
    print("=" * 60)

    # Use a random test user ID
    test_user_id = str(uuid4())
    print(f"Test User ID: {test_user_id}\n")

    # Test 1: Add Task
    print("1️⃣  Testing add_task...")
    try:
        result = await add_task(
            user_id=test_user_id,
            title="Test MCP Task",
            description="Testing MCP tool implementation"
        )
        print(f"✅ {result}")

        # Extract task_id from response
        task_id = result.split("ID: ")[1].rstrip(")")
        print(f"   Task ID: {task_id}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return

    # Test 2: Add Second Task
    print("2️⃣  Testing add_task (second task)...")
    try:
        result = await add_task(
            user_id=test_user_id,
            title="Complete documentation",
            description="Write comprehensive docs for MCP server"
        )
        print(f"✅ {result}")

        task_id_2 = result.split("ID: ")[1].rstrip(")")
        print(f"   Task ID: {task_id_2}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return

    # Test 3: List All Tasks
    print("3️⃣  Testing list_tasks (all)...")
    try:
        result = await list_tasks(user_id=test_user_id, status="all")
        print(f"✅ {result}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # Test 4: List Pending Tasks
    print("4️⃣  Testing list_tasks (pending)...")
    try:
        result = await list_tasks(user_id=test_user_id, status="pending")
        print(f"✅ {result}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # Test 5: Update Task
    print("5️⃣  Testing update_task...")
    try:
        result = await update_task(
            user_id=test_user_id,
            task_id=task_id,
            title="Updated MCP Task",
            description="Updated description for testing"
        )
        print(f"✅ {result}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # Test 6: Update Task (title only)
    print("6️⃣  Testing update_task (title only)...")
    try:
        result = await update_task(
            user_id=test_user_id,
            task_id=task_id_2,
            title="Complete MCP documentation"
        )
        print(f"✅ {result}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # Test 7: Complete Task
    print("7️⃣  Testing complete_task...")
    try:
        result = await complete_task(
            user_id=test_user_id,
            task_id=task_id
        )
        print(f"✅ {result}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # Test 8: List Completed Tasks
    print("8️⃣  Testing list_tasks (completed)...")
    try:
        result = await list_tasks(user_id=test_user_id, status="completed")
        print(f"✅ {result}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # Test 9: List Pending Tasks (should show only task_id_2)
    print("9️⃣  Testing list_tasks (pending after completion)...")
    try:
        result = await list_tasks(user_id=test_user_id, status="pending")
        print(f"✅ {result}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # Test 10: Delete Task
    print("🔟 Testing delete_task...")
    try:
        result = await delete_task(
            user_id=test_user_id,
            task_id=task_id
        )
        print(f"✅ {result}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # Test 11: Verify Deletion
    print("1️⃣1️⃣  Testing list_tasks (after deletion)...")
    try:
        result = await list_tasks(user_id=test_user_id, status="all")
        print(f"✅ {result}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # Test 12: Delete Remaining Task
    print("1️⃣2️⃣  Testing delete_task (cleanup)...")
    try:
        result = await delete_task(
            user_id=test_user_id,
            task_id=task_id_2
        )
        print(f"✅ {result}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # Error Scenarios
    print("=" * 60)
    print("\n🔴 Testing Error Scenarios\n")
    print("=" * 60)

    # Error Test 1: Task Not Found
    print("\n1️⃣  Testing error case (task not found)...")
    try:
        fake_task_id = str(uuid4())
        result = await complete_task(
            user_id=test_user_id,
            task_id=fake_task_id
        )
        print(f"❌ Should have raised error: {result}")
    except ValueError as e:
        print(f"✅ Error handled correctly: {e}")

    # Error Test 2: Invalid UUID Format
    print("\n2️⃣  Testing error case (invalid UUID)...")
    try:
        result = await add_task(
            user_id="invalid-uuid",
            title="Test Task"
        )
        print(f"❌ Should have raised error: {result}")
    except ValueError as e:
        print(f"✅ Error handled correctly: {e}")

    # Error Test 3: Invalid Status Filter
    print("\n3️⃣  Testing error case (invalid status filter)...")
    try:
        result = await list_tasks(
            user_id=test_user_id,
            status="invalid_status"
        )
        print(f"❌ Should have raised error: {result}")
    except ValueError as e:
        print(f"✅ Error handled correctly: {e}")

    # Error Test 4: Empty Title
    print("\n4️⃣  Testing error case (empty title)...")
    try:
        result = await add_task(
            user_id=test_user_id,
            title=""
        )
        print(f"❌ Should have raised error: {result}")
    except ValueError as e:
        print(f"✅ Error handled correctly: {e}")

    # Error Test 5: Title Too Long
    print("\n5️⃣  Testing error case (title too long)...")
    try:
        result = await add_task(
            user_id=test_user_id,
            title="x" * 201  # Exceeds 200 character limit
        )
        print(f"❌ Should have raised error: {result}")
    except ValueError as e:
        print(f"✅ Error handled correctly: {e}")

    # Error Test 6: Update with No Fields
    print("\n6️⃣  Testing error case (update with no fields)...")
    try:
        result = await update_task(
            user_id=test_user_id,
            task_id=str(uuid4())
        )
        print(f"❌ Should have raised error: {result}")
    except ValueError as e:
        print(f"✅ Error handled correctly: {e}")

    # Error Test 7: Permission Denied (different user)
    print("\n7️⃣  Testing error case (permission denied)...")
    try:
        # Create task for test user
        result = await add_task(
            user_id=test_user_id,
            title="User isolation test"
        )
        perm_task_id = result.split("ID: ")[1].rstrip(")")

        # Try to access with different user ID
        different_user_id = str(uuid4())
        result = await complete_task(
            user_id=different_user_id,
            task_id=perm_task_id
        )
        print(f"❌ Should have raised error: {result}")
    except ValueError as e:
        print(f"✅ Error handled correctly: {e}")

    print("\n" + "=" * 60)
    print("\n🎉 All MCP tool tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_tools())
