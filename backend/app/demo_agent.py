"""
Demo Math Agent using OpenAI Agents SDK with Gemini 2.0 Flash

This module demonstrates the correct pattern for using the OpenAI Agents SDK
with Gemini API. It serves as a reference for refactoring the TodoBot agent.

Usage:
    python -m app.demo_agent
"""

import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled

# Load environment variables
load_dotenv()


# Tool definition using @function_tool decorator
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


async def test_gemini_connectivity():
    """Test Gemini API connectivity with a simple math agent."""

    # Disable tracing to avoid SDK interference
    set_tracing_disabled(True)

    # Get Gemini API key from environment
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    # Initialize AsyncOpenAI with Gemini base URL
    provider = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )

    # Configure model using OpenAIChatCompletionsModel
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
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
        "Calculate 8 times 9",
        "Add 100 and 200, then multiply the result by 3"
    ]

    print("\n" + "="*60)
    print("Testing Gemini Connectivity with Math Agent")
    print("="*60 + "\n")

    for query in test_queries:
        print(f"Query: {query}")

        try:
            # Execute agent through Runner.run()
            result = await Runner.run(math_agent, query)

            # Access final output from result
            print(f"Response: {result.final_output}")
            print(f"Tool calls made: {len(result.tool_calls) if hasattr(result, 'tool_calls') else 0}")
            print("-" * 60)

        except Exception as e:
            print(f"ERROR: {e}")
            print("-" * 60)
            raise

    print("\n✅ Gemini connectivity test PASSED\n")
    return True


if __name__ == "__main__":
    asyncio.run(test_gemini_connectivity())
