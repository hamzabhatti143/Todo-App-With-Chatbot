import asyncio
import httpx

async def test():
    async with httpx.AsyncClient() as client:
        # Login
        r = await client.post('http://localhost:8000/api/auth/login',
            json={'email': 'test_chat_user@example.com', 'password': 'SecurePassword123!'})
        token = r.json()['access_token']
        print(f"Token: {token[:30]}...")

        # Send chat
        r2 = await client.post('http://localhost:8000/api/chat',
            json={'content': 'Add buy milk'},
            headers={'Authorization': f'Bearer {token}'})

        print(f"Status: {r2.status_code}")
        print(f"Response: {r2.text}")

asyncio.run(test())
