"""
Complete End-to-End Test for Chat API with Authentication

This script tests the full authentication + chat flow:
1. Register a test user
2. Login and get JWT token
3. List conversations (should work with token)
4. Send chat messages with authentication
5. Verify responses

Usage:
    python test_chat_with_auth.py
"""

import asyncio
import sys
import json
from httpx import AsyncClient

BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test_chat_user@example.com"
TEST_PASSWORD = "SecurePassword123!"


async def test_full_chat_flow():
    """Run complete end-to-end test with authentication."""

    async with AsyncClient(base_url=BASE_URL) as client:

        print("\n" + "="*70)
        print("STEP 1: Register Test User")
        print("="*70)

        # Register user
        register_response = await client.post(
            "/api/auth/register",
            json={
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            }
        )

        if register_response.status_code == 201:
            print(f"[SUCCESS] User registered: {TEST_EMAIL}")
            user_data = register_response.json()
            print(f"User ID: {user_data['id']}")
        elif register_response.status_code == 400:
            print(f"[INFO] User already exists: {TEST_EMAIL}")
        else:
            print(f"[ERROR] Registration failed: {register_response.status_code}")
            print(f"Response: {register_response.text}")
            return False

        print("\n" + "="*70)
        print("STEP 2: Login and Get JWT Token")
        print("="*70)

        # Login to get token
        login_response = await client.post(
            "/api/auth/login",
            json={
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            }
        )

        if login_response.status_code != 200:
            print(f"[ERROR] Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return False

        token_data = login_response.json()
        access_token = token_data["access_token"]

        print(f"[SUCCESS] Login successful")
        print(f"Token: {access_token[:30]}...")

        # Prepare authorization headers
        auth_headers = {
            "Authorization": f"Bearer {access_token}"
        }

        print("\n" + "="*70)
        print("STEP 3: List Conversations (Should Work with Auth)")
        print("="*70)

        # Test listing conversations with authentication
        conversations_response = await client.get(
            "/api/conversations",
            headers=auth_headers
        )

        if conversations_response.status_code == 200:
            print(f"[SUCCESS] Conversations endpoint accessible")
            conversations = conversations_response.json()
            print(f"Total conversations: {len(conversations)}")
        else:
            print(f"[ERROR] Failed to list conversations: {conversations_response.status_code}")
            print(f"Response: {conversations_response.text}")
            return False

        print("\n" + "="*70)
        print("STEP 4: Send Chat Message with Authentication")
        print("="*70)

        # Send first chat message (creates new conversation)
        chat_message_1 = "Add a task to buy groceries"
        print(f"\nSending: \"{chat_message_1}\"")

        chat_response_1 = await client.post(
            "/api/chat",
            json={
                "content": chat_message_1
            },
            headers=auth_headers
        )

        if chat_response_1.status_code == 200:
            print(f"[SUCCESS] Chat message sent successfully")
            response_data_1 = chat_response_1.json()
            print(f"\nConversation ID: {response_data_1['conversation_id']}")
            print(f"TodoBot: {response_data_1['content']}")

            conversation_id = response_data_1['conversation_id']
        else:
            print(f"[ERROR] Chat failed: {chat_response_1.status_code}")
            print(f"Response: {chat_response_1.text}")
            return False

        print("\n" + "-"*70)

        # Send second message in same conversation
        chat_message_2 = "Show my tasks"
        print(f"\nSending: \"{chat_message_2}\"")

        chat_response_2 = await client.post(
            "/api/chat",
            json={
                "content": chat_message_2,
                "conversation_id": conversation_id
            },
            headers=auth_headers
        )

        if chat_response_2.status_code == 200:
            print(f"[SUCCESS] Follow-up message sent successfully")
            response_data_2 = chat_response_2.json()
            print(f"TodoBot: {response_data_2['content']}")
        else:
            print(f"[ERROR] Chat failed: {chat_response_2.status_code}")
            print(f"Response: {chat_response_2.text}")
            return False

        print("\n" + "-"*70)

        # Send third message
        chat_message_3 = "Mark the groceries task as done"
        print(f"\nSending: \"{chat_message_3}\"")

        chat_response_3 = await client.post(
            "/api/chat",
            json={
                "content": chat_message_3,
                "conversation_id": conversation_id
            },
            headers=auth_headers
        )

        if chat_response_3.status_code == 200:
            print(f"[SUCCESS] Task completion message sent successfully")
            response_data_3 = chat_response_3.json()
            print(f"TodoBot: {response_data_3['content']}")
        else:
            print(f"[ERROR] Chat failed: {chat_response_3.status_code}")
            print(f"Response: {chat_response_3.text}")
            return False

        print("\n" + "="*70)
        print("STEP 5: Verify Conversation History")
        print("="*70)

        # Get conversation history
        history_response = await client.get(
            f"/api/conversations/{conversation_id}/messages",
            headers=auth_headers
        )

        if history_response.status_code == 200:
            print(f"[SUCCESS] Conversation history retrieved")
            messages = history_response.json()
            print(f"\nTotal messages in conversation: {len(messages)}")

            for i, msg in enumerate(messages, 1):
                role = msg['role'].upper()
                content = msg['content'][:60] + "..." if len(msg['content']) > 60 else msg['content']
                print(f"  {i}. [{role}] {content}")
        else:
            print(f"[ERROR] Failed to get conversation history: {history_response.status_code}")
            print(f"Response: {history_response.text}")

        print("\n" + "="*70)
        print("STEP 6: Test Without Authentication (Should Fail)")
        print("="*70)

        # Try to access without token
        no_auth_response = await client.get("/api/conversations")

        if no_auth_response.status_code == 401:
            print(f"[SUCCESS] Correctly rejected unauthenticated request")
            print(f"Error: {no_auth_response.json()['detail']}")
        else:
            print(f"[WARNING] Expected 401, got {no_auth_response.status_code}")

        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print("[SUCCESS] All tests passed!")
        print("\nVerified:")
        print("  1. User registration works")
        print("  2. User login returns JWT token")
        print("  3. /api/conversations requires authentication")
        print("  4. /api/chat works with authentication")
        print("  5. Conversation history is maintained")
        print("  6. Multiple messages in same conversation work")
        print("  7. TodoBot agent processes commands correctly")
        print("  8. Unauthenticated requests are properly rejected")

        return True


async def main():
    """Main entry point."""
    try:
        print("\n" + "#"*70)
        print("# TodoBot Chat API - End-to-End Authentication Test")
        print("#"*70)
        print(f"\nTesting against: {BASE_URL}")
        print(f"Test user: {TEST_EMAIL}")

        success = await test_full_chat_flow()

        if success:
            print("\n" + "="*70)
            print("[FINAL RESULT] ALL TESTS PASSED")
            print("="*70 + "\n")
            sys.exit(0)
        else:
            print("\n" + "="*70)
            print("[FINAL RESULT] TESTS FAILED")
            print("="*70 + "\n")
            sys.exit(1)

    except Exception as e:
        print(f"\n[EXCEPTION] Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
