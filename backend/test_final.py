import asyncio
import httpx

async def test():
    async with httpx.AsyncClient(base_url="http://localhost:8001", timeout=30.0) as client:
        print("\n=== Step 1: Login ===")
        r = await client.post('/api/auth/login',
            json={'email': 'test_chat_user@example.com', 'password': 'SecurePassword123!'})

        if r.status_code != 200:
            print(f"Login failed: {r.status_code}")
            print(r.text)
            return

        token = r.json()['access_token']
        print(f"Login successful. Token: {token[:30]}...")

        print("\n=== Step 2: Send chat message ===")
        r2 = await client.post('/api/chat',
            json={'content': 'Add buy milk'},
            headers={'Authorization': f'Bearer {token}'})

        print(f"Status: {r2.status_code}")

        if r2.status_code == 200:
            data = r2.json()
            print(f"SUCCESS! Response:")
            print(f"  Conversation ID: {data.get('conversation_id')}")
            print(f"  Message: {data.get('content')}")
        else:
            print(f"ERROR: {r2.text}")
            try:
                print(f"JSON: {r2.json()}")
            except:
                pass

asyncio.run(test())
