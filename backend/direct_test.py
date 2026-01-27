"""
Direct test of chat endpoint by calling the function directly
"""
import asyncio
import sys
from uuid import uuid4

# Set up path
sys.path.insert(0, '/mnt/d/todo-fullstack-web/backend')

from app.agent import TodoBot, AgentRequest
from app.schemas.chat import ChatMessageRequest
from app.models.user import User
from app.database import get_session
from sqlmodel import Session, select

async def test_chat_direct():
    """Test chat endpoint directly without HTTP."""

    # Get test user
    session = next(get_session())
    user = session.exec(select(User).where(User.email == "test_chat_user@example.com")).first()

    if not user:
        print("User not found!")
        return

    print(f"Test user: {user.email} (ID: {user.id})")

    # Create chat request
    request = ChatMessageRequest(
        content="Add buy milk"
    )

    print(f"\nSending message: '{request.content}'")

    # Import and call the chat function directly
    try:
        from app.routes.chat import send_chat_message
        from app.middleware.rate_limit import limiter

        # Create fake request object for rate limiter
        class FakeRequest:
            client = type('obj', (object,), {'host': '127.0.0.1'})

        # Call the endpoint
        result = await send_chat_message(
            request=request,
            current_user=user,
            session=session
        )

        print(f"\n[SUCCESS] Chat response received:")
        print(f"Conversation ID: {result.conversation_id}")
        print(f"Content: {result.content}")

    except Exception as e:
        print(f"\n[ERROR] Exception occurred:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test_chat_direct())
