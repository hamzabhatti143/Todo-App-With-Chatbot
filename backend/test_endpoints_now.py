#!/usr/bin/env python3
"""Test chat and conversations endpoints with fresh token."""

import requests

BASE_URL = "http://localhost:8002"

print("="*70)
print("TESTING ENDPOINTS WITH FRESH TOKEN")
print("="*70)

# Step 1: Login to get fresh token
print("\n[1/3] Logging in to get fresh token...")
login_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={
        "email": "test_chat_user@example.com",
        "password": "SecurePassword123!"
    }
)

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print(f"[OK] Login successful")
    print(f"    Token: {token[:30]}...")
else:
    print(f"[FAIL] Login failed: {login_response.status_code}")
    print(f"    {login_response.json()}")
    exit(1)

headers = {"Authorization": f"Bearer {token}"}

# Step 2: Test GET /api/conversations
print("\n[2/3] Testing GET /api/conversations...")
conv_response = requests.get(f"{BASE_URL}/api/conversations", headers=headers)

print(f"    Status: {conv_response.status_code}")
if conv_response.status_code == 200:
    conversations = conv_response.json()
    print(f"[OK] GET /api/conversations - SUCCESS")
    print(f"    Found {len(conversations)} conversations")
    if conversations:
        for conv in conversations[:3]:
            print(f"    - {conv.get('title', 'Untitled')}")
else:
    print(f"[FAIL] GET /api/conversations - FAILED")
    print(f"    {conv_response.json()}")

# Step 3: Test POST /api/chat
print("\n[3/3] Testing POST /api/chat...")
chat_response = requests.post(
    f"{BASE_URL}/api/chat",
    headers=headers,
    json={"content": "Test message - what time is it?"}
)

print(f"    Status: {chat_response.status_code}")
if chat_response.status_code == 200:
    chat_data = chat_response.json()
    print(f"[OK] POST /api/chat - SUCCESS")
    print(f"    Conversation ID: {chat_data['conversation_id']}")
    print(f"    Response: {chat_data['content'][:100]}...")
else:
    print(f"[FAIL] POST /api/chat - FAILED")
    print(f"    {chat_response.json()}")

print("\n" + "="*70)
print("ENDPOINT TEST RESULTS")
print("="*70)
print(f"GET /api/conversations: {'[OK] WORKING' if conv_response.status_code == 200 else '[FAIL] FAILED'}")
print(f"POST /api/chat: {'[OK] WORKING' if chat_response.status_code == 200 else '[FAIL] FAILED'}")
print("="*70)

if conv_response.status_code == 200 and chat_response.status_code == 200:
    print("\n[SUCCESS] BOTH ENDPOINTS WORKING PERFECTLY!")
    print("\nThe issue is in YOUR BROWSER - old token in localStorage")
    print("\nTO FIX:")
    print("1. Open browser at http://localhost:3000")
    print("2. Press F12 -> Console")
    print("3. Run: localStorage.clear(); location.reload();")
    print("4. Login again with test credentials")
    print("\nThen it will work!")
else:
    print("\n[WARNING] Backend has issues - check logs")
