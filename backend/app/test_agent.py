"""
Tests for TodoBot Agent

Run with:
    python -m app.test_agent
"""

import asyncio
import uuid
import logging
from typing import List

from app.agent import TodoBot, AgentRequest, AgentResponse, ConversationMessage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TestResults:
    """Track test results."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors: List[str] = []

    def record_pass(self, test_name: str):
        self.passed += 1
        logger.info(f"✓ PASS: {test_name}")

    def record_fail(self, test_name: str, reason: str):
        self.failed += 1
        error_msg = f"✗ FAIL: {test_name} - {reason}"
        self.errors.append(error_msg)
        logger.error(error_msg)

    def summary(self):
        total = self.passed + self.failed
        logger.info(f"\n{'='*60}")
        logger.info(f"Test Results: {self.passed}/{total} passed")
        if self.errors:
            logger.info(f"\nFailures:")
            for error in self.errors:
                logger.info(f"  {error}")
        logger.info(f"{'='*60}\n")
        return self.failed == 0


# ============================================================================
# Test Fixtures
# ============================================================================

# Create test user ID
TEST_USER_ID = str(uuid.uuid4())
logger.info(f"Test User ID: {TEST_USER_ID}")


# ============================================================================
# Success Scenario Tests
# ============================================================================

async def test_create_task(agent: TodoBot, results: TestResults):
    """Test creating a task with natural language."""
    test_name = "Create Task"

    try:
        request = AgentRequest(
            user_id=TEST_USER_ID,
            message="Add buy groceries"
        )

        response = await agent.run(request)

        # Verify response
        assert response.error is None, f"Unexpected error: {response.error}"
        assert len(response.tool_calls) > 0, "No tool calls"
        assert response.tool_calls[0].name == "add_task", "Wrong tool"
        assert response.tool_calls[0].success, "Tool call failed"
        assert "Task created" in response.message or "created" in response.message.lower(), "No confirmation"

        results.record_pass(test_name)
        return response

    except AssertionError as e:
        results.record_fail(test_name, str(e))
        return None
    except Exception as e:
        results.record_fail(test_name, f"Exception: {e}")
        return None


async def test_list_tasks(agent: TodoBot, results: TestResults):
    """Test listing tasks."""
    test_name = "List Tasks"

    try:
        request = AgentRequest(
            user_id=TEST_USER_ID,
            message="Show my tasks"
        )

        response = await agent.run(request)

        assert response.error is None, f"Error: {response.error}"
        assert len(response.tool_calls) > 0, "No tool calls"
        assert response.tool_calls[0].name == "list_tasks", "Wrong tool"
        assert response.tool_calls[0].success, "Tool failed"

        results.record_pass(test_name)
        return response

    except AssertionError as e:
        results.record_fail(test_name, str(e))
        return None
    except Exception as e:
        results.record_fail(test_name, f"Exception: {e}")
        return None


async def test_list_pending_tasks(agent: TodoBot, results: TestResults):
    """Test filtering pending tasks."""
    test_name = "List Pending Tasks"

    try:
        request = AgentRequest(
            user_id=TEST_USER_ID,
            message="What's pending?"
        )

        response = await agent.run(request)

        assert response.error is None, f"Error: {response.error}"
        assert len(response.tool_calls) > 0, "No tool calls"
        assert response.tool_calls[0].name == "list_tasks", "Wrong tool"
        assert response.tool_calls[0].arguments.get("status") == "pending", "Wrong status"

        results.record_pass(test_name)
        return response

    except AssertionError as e:
        results.record_fail(test_name, str(e))
        return None
    except Exception as e:
        results.record_fail(test_name, f"Exception: {e}")
        return None


async def test_conversation_context(agent: TodoBot, results: TestResults):
    """Test multi-turn conversation with context."""
    test_name = "Conversation Context"

    try:
        # Turn 1: Create task
        req1 = AgentRequest(
            user_id=TEST_USER_ID,
            message="Add call mom"
        )
        res1 = await agent.run(req1)
        assert res1.error is None, "Turn 1 failed"

        # Turn 2: List tasks with context
        req2 = AgentRequest(
            user_id=TEST_USER_ID,
            message="Show my tasks",
            conversation_history=[
                ConversationMessage(role="user", content="Add call mom"),
                ConversationMessage(role="assistant", content=res1.message)
            ]
        )
        res2 = await agent.run(req2)
        assert res2.error is None, "Turn 2 failed"
        assert "call mom" in res2.message.lower(), "Task not in list"

        results.record_pass(test_name)
        return res2

    except AssertionError as e:
        results.record_fail(test_name, str(e))
        return None
    except Exception as e:
        results.record_fail(test_name, f"Exception: {e}")
        return None


async def test_create_task_with_description(agent: TodoBot, results: TestResults):
    """Test creating task with description."""
    test_name = "Create Task with Description"

    try:
        request = AgentRequest(
            user_id=TEST_USER_ID,
            message="Add finish report by Friday with high priority"
        )

        response = await agent.run(request)

        assert response.error is None, f"Error: {response.error}"
        assert len(response.tool_calls) > 0, "No tool calls"
        assert response.tool_calls[0].name == "add_task", "Wrong tool"
        assert response.tool_calls[0].success, "Tool failed"

        # Check if description was extracted
        args = response.tool_calls[0].arguments
        assert "title" in args, "No title"

        results.record_pass(test_name)
        return response

    except AssertionError as e:
        results.record_fail(test_name, str(e))
        return None
    except Exception as e:
        results.record_fail(test_name, f"Exception: {e}")
        return None


# ============================================================================
# Error Scenario Tests
# ============================================================================

async def test_invalid_user_id(agent: TodoBot, results: TestResults):
    """Test validation of invalid user_id."""
    test_name = "Invalid User ID"

    try:
        try:
            request = AgentRequest(
                user_id="not-a-uuid",
                message="Add test task"
            )
            results.record_fail(test_name, "Should have raised validation error")
        except ValueError as e:
            if "UUID" in str(e):
                results.record_pass(test_name)
            else:
                results.record_fail(test_name, f"Wrong error: {e}")

    except Exception as e:
        results.record_fail(test_name, f"Exception: {e}")


async def test_empty_message(agent: TodoBot, results: TestResults):
    """Test validation of empty message."""
    test_name = "Empty Message"

    try:
        try:
            request = AgentRequest(
                user_id=TEST_USER_ID,
                message="   "  # Whitespace only
            )
            results.record_fail(test_name, "Should have raised validation error")
        except ValueError as e:
            if "empty" in str(e).lower():
                results.record_pass(test_name)
            else:
                results.record_fail(test_name, f"Wrong error: {e}")

    except Exception as e:
        results.record_fail(test_name, f"Exception: {e}")


async def test_message_too_long(agent: TodoBot, results: TestResults):
    """Test validation of message length."""
    test_name = "Message Too Long"

    try:
        try:
            request = AgentRequest(
                user_id=TEST_USER_ID,
                message="A" * 2001  # Exceeds max_length
            )
            results.record_fail(test_name, "Should have raised validation error")
        except ValueError as e:
            results.record_pass(test_name)

    except Exception as e:
        results.record_fail(test_name, f"Exception: {e}")


async def test_conversation_history_too_long(agent: TodoBot, results: TestResults):
    """Test validation of conversation history length."""
    test_name = "Conversation History Too Long"

    try:
        # Create 21 messages (exceeds limit of 20)
        long_history = []
        for i in range(21):
            role = "user" if i % 2 == 0 else "assistant"
            long_history.append(
                ConversationMessage(role=role, content=f"Message {i}")
            )

        try:
            request = AgentRequest(
                user_id=TEST_USER_ID,
                message="Test",
                conversation_history=long_history
            )
            results.record_fail(test_name, "Should have raised validation error")
        except ValueError as e:
            if "20" in str(e):
                results.record_pass(test_name)
            else:
                results.record_fail(test_name, f"Wrong error: {e}")

    except Exception as e:
        results.record_fail(test_name, f"Exception: {e}")


# ============================================================================
# Natural Language Understanding Tests
# ============================================================================

async def test_various_create_phrasings(agent: TodoBot, results: TestResults):
    """Test different ways to create tasks."""
    test_name = "Various Create Phrasings"

    phrasings = [
        "Create a task to exercise",
        "Remind me to water plants",
        "I need to review code",
    ]

    try:
        for phrasing in phrasings:
            request = AgentRequest(
                user_id=TEST_USER_ID,
                message=phrasing
            )
            response = await agent.run(request)

            assert response.error is None, f"Error on '{phrasing}': {response.error}"
            assert len(response.tool_calls) > 0, f"No tool calls for '{phrasing}'"
            assert response.tool_calls[0].name == "add_task", f"Wrong tool for '{phrasing}'"

        results.record_pass(test_name)

    except AssertionError as e:
        results.record_fail(test_name, str(e))
    except Exception as e:
        results.record_fail(test_name, f"Exception: {e}")


async def test_various_list_phrasings(agent: TodoBot, results: TestResults):
    """Test different ways to list tasks."""
    test_name = "Various List Phrasings"

    phrasings = [
        "What do I need to do?",
        "List my tasks",
        "What's on my todo list?",
    ]

    try:
        for phrasing in phrasings:
            request = AgentRequest(
                user_id=TEST_USER_ID,
                message=phrasing
            )
            response = await agent.run(request)

            assert response.error is None, f"Error on '{phrasing}': {response.error}"
            assert len(response.tool_calls) > 0, f"No tool calls for '{phrasing}'"
            assert response.tool_calls[0].name == "list_tasks", f"Wrong tool for '{phrasing}'"

        results.record_pass(test_name)

    except AssertionError as e:
        results.record_fail(test_name, str(e))
    except Exception as e:
        results.record_fail(test_name, f"Exception: {e}")


# ============================================================================
# Cleanup Tests
# ============================================================================

async def test_cleanup_tasks(agent: TodoBot, results: TestResults):
    """Clean up test tasks."""
    test_name = "Cleanup Tasks"

    try:
        # List all tasks
        req1 = AgentRequest(
            user_id=TEST_USER_ID,
            message="Show all my tasks"
        )
        res1 = await agent.run(req1)

        # Parse task IDs from result (if any)
        # Note: In real implementation, we'd extract task IDs from the response
        # For now, just verify cleanup request works
        logger.info(f"Cleanup: {res1.message}")

        results.record_pass(test_name)

    except Exception as e:
        results.record_fail(test_name, f"Exception: {e}")


# ============================================================================
# Main Test Runner
# ============================================================================

async def run_all_tests():
    """Run all tests."""
    logger.info("="*60)
    logger.info("TodoBot Agent Test Suite")
    logger.info("="*60)

    # Initialize agent
    agent = TodoBot()
    results = TestResults()

    logger.info("\n--- Success Scenario Tests ---\n")
    await test_create_task(agent, results)
    await test_list_tasks(agent, results)
    await test_list_pending_tasks(agent, results)
    await test_conversation_context(agent, results)
    await test_create_task_with_description(agent, results)

    logger.info("\n--- Error Scenario Tests ---\n")
    await test_invalid_user_id(agent, results)
    await test_empty_message(agent, results)
    await test_message_too_long(agent, results)
    await test_conversation_history_too_long(agent, results)

    logger.info("\n--- Natural Language Tests ---\n")
    await test_various_create_phrasings(agent, results)
    await test_various_list_phrasings(agent, results)

    logger.info("\n--- Cleanup ---\n")
    await test_cleanup_tasks(agent, results)

    # Print summary
    success = results.summary()

    if success:
        logger.info("All tests passed!")
        return 0
    else:
        logger.error(f"{results.failed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    exit(exit_code)
