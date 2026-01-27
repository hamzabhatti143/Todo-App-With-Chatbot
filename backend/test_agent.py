"""
Test the refactored TodoBot agent
"""

import asyncio
import sys
sys.path.insert(0, '/mnt/d/todo-fullstack-web/backend')

from app.agent import TodoBot, AgentRequest


async def test_agent():
    """Test TodoBot with simple commands."""

    print("\n" + "="*60)
    print("Testing TodoBot Agent")
    print("="*60 + "\n")

    # Initialize agent
    agent = TodoBot()
    print("[OK] TodoBot initialized\n")

    # Test user ID (would come from JWT in real usage)
    test_user_id = "550e8400-e29b-41d4-a716-446655440000"

    # Test queries
    test_queries = [
        "Add a task to buy groceries",
        "Show my tasks",
    ]

    for query in test_queries:
        print(f"Query: {query}")

        try:
            request = AgentRequest(
                user_id=test_user_id,
                message=query
            )

            response = await agent.run(request)

            print(f"Response: {response.message}")
            print(f"Error: {response.error}")
            print("-" * 60 + "\n")

        except Exception as e:
            print(f"ERROR: {e}")
            print("-" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(test_agent())
