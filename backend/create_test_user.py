#!/usr/bin/env python3
"""Create a test user for testing the chat API."""

import requests
import sys

BASE_URL = "http://localhost:8002"

def create_test_user():
    """Create a test user account."""
    user_data = {
        "email": "test_chat_user@example.com",
        "password": "SecurePassword123!"
    }

    try:
        # Try to register
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)

        if response.status_code == 201:
            print("[OK] Test user created successfully")
            user = response.json()
            print(f"  User ID: {user['id']}")
            print(f"  Email: {user['email']}")
            return True
        elif response.status_code == 400 and "already registered" in response.json().get("detail", "").lower():
            print("[OK] Test user already exists")
            return True
        else:
            print(f"[FAIL] Failed to create user: {response.status_code}")
            print(f"  Error: {response.json()}")
            return False

    except Exception as e:
        print(f"[FAIL] Error creating user: {e}")
        return False

def test_login():
    """Test login with the test user."""
    login_data = {
        "email": "test_chat_user@example.com",
        "password": "SecurePassword123!"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)

        if response.status_code == 200:
            print("\n[OK] Login successful")
            token_data = response.json()
            token = token_data.get("access_token")
            print(f"  Token: {token[:20]}...")
            return token
        else:
            print(f"\n[FAIL] Login failed: {response.status_code}")
            print(f"  Error: {response.json()}")
            return None

    except Exception as e:
        print(f"\n[FAIL] Login error: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("Test User Setup")
    print("=" * 60)

    if create_test_user():
        token = test_login()
        if token:
            print("\n" + "=" * 60)
            print("Setup complete! You can now test the chat API.")
            print("=" * 60)
            sys.exit(0)

    sys.exit(1)
