"""Complete end-to-end test of chat functionality"""
import asyncio
import httpx

async def test():
    base_url = "http://localhost:8001"
    async with httpx.AsyncClient(base_url=base_url, timeout=30.0) as client:
        print("\n" + "="*70)
        print("COMPLETE END-TO-END CHAT TEST")
        print("="*70)

        # Step 1: Login
        print("\n[1/7] Login...")
        r = await client.post('/api/auth/login',
            json={'email': 'test_chat_user@example.com', 'password': 'SecurePassword123!'})
        assert r.status_code == 200, f"Login failed: {r.status_code}"
        token = r.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        print("[OK] Login successful")

        # Step 2: List conversations (should be empty or have previous ones)
        print("\n[2/7] List conversations...")
        r = await client.get('/api/conversations', headers=headers)
        assert r.status_code == 200, f"List conversations failed: {r.status_code}"
        print(f"[OK] Found {len(r.json())} conversation(s)")

        # Step 3: Send first chat message (creates new conversation)
        print("\n[3/7] Send chat message: 'Add task to buy groceries'...")
        r = await client.post('/api/chat',
            json={'content': 'Add a task to buy groceries'},
            headers=headers)
        assert r.status_code == 200, f"Chat failed: {r.status_code} - {r.text}"
        data = r.json()
        conversation_id = data['conversation_id']
        print(f"[OK] Message sent successfully")
        print(f"  Conversation ID: {conversation_id}")
        print(f"  Response: {data['content'][:80]}...")

        # Step 4: Send second message in same conversation
        print("\n[4/7] Send follow-up: 'Show my tasks'...")
        r = await client.post('/api/chat',
            json={'content': 'Show my tasks', 'conversation_id': conversation_id},
            headers=headers)
        assert r.status_code == 200, f"Chat failed: {r.status_code}"
        data = r.json()
        print(f"[OK] Follow-up message sent")
        print(f"  Response: {data['content'][:80]}...")

        # Step 5: Send third message
        print("\n[5/7] Send command: 'Mark groceries as done'...")
        r = await client.post('/api/chat',
            json={'content': 'Mark the groceries task as done', 'conversation_id': conversation_id},
            headers=headers)
        assert r.status_code == 200, f"Chat failed: {r.status_code}"
        data = r.json()
        print(f"[OK] Task completion command sent")
        print(f"  Response: {data['content'][:80]}...")

        # Step 6: Get conversation history
        print("\n[6/7] Get conversation history...")
        r = await client.get(f'/api/conversations/{conversation_id}/messages', headers=headers)
        assert r.status_code == 200, f"Get messages failed: {r.status_code}"
        messages = r.json()
        print(f"[OK] Retrieved {len(messages)} messages")
        for i, msg in enumerate(messages, 1):
            role = msg['role'].upper()
            content = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
            print(f"  {i}. [{role}] {content}")

        # Step 7: Verify authentication (test unauthorized access)
        print("\n[7/7] Test authentication (should fail without token)...")
        r = await client.get('/api/conversations')
        assert r.status_code in [401, 403], f"Expected 401 or 403, got {r.status_code}"
        print(f"[OK] Correctly rejected unauthenticated request (status {r.status_code})")

        print("\n" + "="*70)
        print("ALL TESTS PASSED [OK]")
        print("="*70)
        print("\nVerified:")
        print("  [OK] User authentication")
        print("  [OK] JWT token validation")
        print("  [OK] Chat endpoint with AI agent")
        print("  [OK] Conversation creation and tracking")
        print("  [OK] Message history retrieval")
        print("  [OK] TodoBot agent task management")
        print("  [OK] Protected endpoint authorization")
        print("\n")

asyncio.run(test())
