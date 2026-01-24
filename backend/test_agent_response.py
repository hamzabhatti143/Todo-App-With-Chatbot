"""Test agent and save response to file"""
import asyncio
from app.agent import TodoBot, AgentRequest

async def test_agent():
    try:
        agent = TodoBot()

        request = AgentRequest(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            message="Add buy groceries"
        )

        response = await agent.run(request)

        # Save to file
        with open("agent_response.txt", "w", encoding="utf-8") as f:
            f.write(f"Message: {response.message}\n\n")
            f.write(f"Tool calls: {len(response.tool_calls)}\n")
            for i, tc in enumerate(response.tool_calls):
                f.write(f"\nTool {i+1}:\n")
                f.write(f"  Name: {tc.name}\n")
                f.write(f"  Success: {tc.success}\n")
                f.write(f"  Result: {tc.result}\n")
                f.write(f"  Args: {tc.arguments}\n")
            f.write(f"\nError: {response.error}\n")

        print("Response saved to agent_response.txt")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_agent())
