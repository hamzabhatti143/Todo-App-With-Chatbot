"""Quick test of TodoBot agent"""
import asyncio
from app.agent import TodoBot, AgentRequest

async def test_agent():
    print("Initializing TodoBot...")
    try:
        agent = TodoBot()
        print("[OK] Agent initialized successfully")

        # Test with a simple message
        request = AgentRequest(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            message="Add buy groceries"
        )

        print("\nSending test message: 'Add buy groceries'")
        response = await agent.run(request)

        print(f"\n[OK] Agent responded:")
        print(f"Message: {response.message}")
        print(f"Tool calls: {len(response.tool_calls)}")
        if response.tool_calls:
            for tc in response.tool_calls:
                print(f"  - {tc.name}: success={tc.success}, result={tc.result[:100]}")
        print(f"Error: {response.error}")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_agent())
