import asyncio
import httpx
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

async def test():
    async with httpx.AsyncClient() as client:
        print("\n=== LOGGING IN ===")
        r = await client.post('http://localhost:8000/api/auth/login',
            json={'email': 'test_chat_user@example.com', 'password': 'SecurePassword123!'})

        if r.status_code != 200:
            print(f"Login failed: {r.status_code}")
            print(r.text)
            return

        token = r.json()['access_token']
        print(f"Login successful. Token: {token[:30]}...")

        print("\n=== SENDING CHAT MESSAGE ===")
        try:
            r2 = await client.post('http://localhost:8000/api/chat',
                json={'content': 'Add buy milk'},
                headers={'Authorization': f'Bearer {token}'},
                timeout=30.0)

            print(f"Chat response status: {r2.status_code}")

            if r2.status_code == 200:
                data = r2.json()
                print(f"Success! Response: {data.get('content', 'No content')}")
            else:
                print(f"Error response: {r2.text}")
                try:
                    print(f"JSON: {r2.json()}")
                except:
                    pass

        except Exception as e:
            print(f"Exception during chat request: {e}")
            import traceback
            traceback.print_exc()

asyncio.run(test())
