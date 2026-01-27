#!/usr/bin/env python3
"""Test script to verify backend connection and authentication."""

import requests
import json

BASE_URL = "http://localhost:8002"

def test_health():
    """Test health endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"[OK] Health check: {response.status_code}")
        print(f"  Response: {response.json()}")
        return True
    except Exception as e:
        print(f"[FAIL] Health check failed: {e}")
        return False

def test_login():
    """Test login and get conversations."""
    try:
        # Login
        login_data = {
            "email": "test_chat_user@example.com",
            "password": "SecurePassword123!"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        print(f"\n[OK] Login: {response.status_code}")

        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("access_token")
            print(f"  Token received: {token[:20]}...")

            # Test conversations endpoint
            headers = {"Authorization": f"Bearer {token}"}
            conv_response = requests.get(f"{BASE_URL}/api/conversations", headers=headers)
            print(f"\n[OK] Get conversations: {conv_response.status_code}")
            if conv_response.status_code == 200:
                conversations = conv_response.json()
                print(f"  Found {len(conversations)} conversations")
                return True
            else:
                print(f"  Error: {conv_response.json()}")
                return False
        else:
            print(f"  Error: {response.json()}")
            return False
    except Exception as e:
        print(f"[FAIL] Login test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Backend Connection Test")
    print("=" * 60)

    if test_health():
        test_login()

    print("\n" + "=" * 60)
