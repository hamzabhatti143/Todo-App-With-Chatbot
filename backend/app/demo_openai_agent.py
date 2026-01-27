"""
Demo Math Agent using OpenAI Agents SDK with OpenAI API

This demonstrates the correct pattern for using the OpenAI Agents SDK.

Usage:
    python -m app.demo_openai_agent
"""

import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled

# Load environment variables
load_dotenv()


# Tool definitions using @function_tool decorator
@function_tool
def add_numbers(a: float, b: float) -> float:
    """
    Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b


@function_tool
def multiply_numbers(a: float, b: float) -> float:
    """
    Multiply two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Product of a and b
    """
    return a * b


async def test_openai_connectivity():
    """Test OpenAI API connectivity with a simple math agent."""

    # Disable tracing to avoid SDK interference
    set_tracing_disabled(True)

    # Get OpenAI API key from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    print(f"[OK] OPENAI_API_KEY loaded: {openai_api_key[:20]}...")

    # Initialize AsyncOpenAI with OpenAI base URL
    provider = AsyncOpenAI(
        api_key=openai_api_key,
        base_url="https://api.openai.com/v1"
    )

    # Configure model using OpenAIChatCompletionsModel
    model = OpenAIChatCompletionsModel(
        model="gpt-4o-mini",
        openai_client=provider
    )

    # Create agent with @function_tool decorated tools
    math_agent = Agent(
        name="MathAgent",
        instructions="You are a helpful math assistant. Use the tools to perform calculations when needed.",
        model=model,
        tools=[add_numbers, multiply_numbers]
    )

    # Test queries
    test_queries = [
        "What is 15 plus 27?",
        "Calculate 8 times 9"
    ]

    print("\n" + "="*60)
    print("Testing OpenAI Connectivity with Math Agent")
    print("="*60 + "\n")

    for query in test_queries:
        print(f"Query: {query}")

        try:
            # Execute agent through Runner.run()
            result = await Runner.run(math_agent, query)

            # Access final output from result
            print(f"Response: {result.final_output}")
            print("-" * 60)

        except Exception as e:
            print(f"ERROR: {e}")
            print("-" * 60)
            raise

    print("\n[SUCCESS] OpenAI connectivity test PASSED\n")
    return True


if __name__ == "__main__":
    asyncio.run(test_openai_connectivity())
