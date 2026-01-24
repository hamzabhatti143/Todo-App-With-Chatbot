"""
Example Agent Usage

This script demonstrates the refactored agent structure following
the universal tool interface pattern similar to OpenAI SDK.

The architecture consists of:
1. Tool Interface (base.py) - Universal contract for all tools
2. Tool Implementations (task_tools.py) - Specific tool logic
3. Agent with Tool Registry - Manages and executes tools
4. Runner Pattern - Async execution with proper error handling

Usage:
    python -m app.example_agent_usage
"""

import asyncio
from decouple import config

from app.agent_refactored import TodoAgent, AgentRequest, AgentConfig


async def main():
    """
    Demonstrate agent usage with the new tool structure.

    This follows the pattern from the demo:
    - Initialize agent with configuration
    - Create request with user input
    - Run agent and get response
    - Display results
    """

    # Initialize agent with configuration
    # Uses Gemini 2.0 Flash as specified in the demo
    agent_config = AgentConfig(
        model_name="gemini-2.0-flash-exp",
        temperature=0.7,
        max_output_tokens=2048
    )

    agent = TodoAgent(config=agent_config)

    # Example user queries
    queries = [
        "Add buy groceries and call mom",
        "Show all my tasks",
        "Complete the groceries task"
    ]

    print("=" * 70)
    print("TodoBot Agent Demo - Refactored Tool Structure")
    print("=" * 70)
    print()

    # Example user_id (in production, this comes from JWT token)
    user_id = "550e8400-e29b-41d4-a716-446655440000"

    for i, query in enumerate(queries, 1):
        print(f"\n{'=' * 70}")
        print(f"Query #{i}: {query}")
        print(f"{'=' * 70}\n")

        # Create request
        request = AgentRequest(
            user_id=user_id,
            message=query
        )

        # Run agent
        response = await agent.run(request)

        # Display response
        print(f"Agent Response:")
        print(f"  {response.message}")
        print()

        # Display tool calls if any
        if response.tool_calls:
            print(f"Tool Calls Executed:")
            for tool_call in response.tool_calls:
                status = "✓ SUCCESS" if tool_call.success else "✗ FAILED"
                print(f"  [{status}] {tool_call.name}")
                print(f"    Arguments: {tool_call.arguments}")
                print(f"    Result: {tool_call.result[:100]}...")
                print()

        # Display errors if any
        if response.error:
            print(f"Error: {response.error}")
            print()

    print("=" * 70)
    print("Demo Complete")
    print("=" * 70)


async def math_agent_demo():
    """
    Demonstrate the pattern from the original demo with math operations.

    This shows how the same architecture would work with different tools.
    Note: Math tools are not implemented, this is just a conceptual demo.
    """

    print("\n" + "=" * 70)
    print("Math Agent Demo - Same Architecture, Different Tools")
    print("=" * 70)
    print()

    # In the demo structure, you would do:
    # from app.tools import AddNumbersTool
    # agent.tool_registry.register(AddNumbersTool())
    #
    # Then run:
    # math_query = "what is the sum of 2+2, 10+10, 4+8?"
    # result = await agent.run(AgentRequest(user_id=user_id, message=math_query))

    print("Architecture Pattern:")
    print("  1. Tool Interface (base.py) - Universal contract")
    print("  2. Tool Implementation (math_tools.py) - Specific logic")
    print("  3. Agent Registration - agent.tool_registry.register(tool)")
    print("  4. Agent Execution - await agent.run(request)")
    print()

    print("The same pattern works for:")
    print("  - Task management tools (current implementation)")
    print("  - Math tools (demo example)")
    print("  - MCP tools (external servers)")
    print("  - HTTP tools (REST API calls)")
    print("  - Custom tools (any domain)")
    print()


if __name__ == "__main__":
    """
    Entry point for the demo.

    Runs both the task management demo and the conceptual math demo
    to show the versatility of the architecture.
    """

    # Run the main todo agent demo
    asyncio.run(main())

    # Show the conceptual pattern demo
    asyncio.run(math_agent_demo())
