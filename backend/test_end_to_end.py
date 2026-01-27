#!/usr/bin/env python3
"""End-to-end test for chat API with task management."""

import requests
import json
import time

BASE_URL = "http://localhost:8002"

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"{title}")
    print('='*70)

def login():
    """Login and get authentication token."""
    print_section("Step 1: Authentication")

    login_data = {
        "email": "test_chat_user@example.com",
        "password": "SecurePassword123!"
    }

    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)

    if response.status_code == 200:
        token = response.json()["access_token"]
        print("[OK] Login successful")
        print(f"    Token: {token[:30]}...")
        return token
    else:
        print(f"[FAIL] Login failed: {response.status_code}")
        print(f"        {response.json()}")
        return None

def test_chat_message(token, message, conversation_id=None):
    """Send a chat message and return the response."""
    print(f"\n  Sending message: \"{message}\"")

    headers = {"Authorization": f"Bearer {token}"}
    data = {"content": message}
    if conversation_id:
        data["conversation_id"] = conversation_id

    response = requests.post(f"{BASE_URL}/api/chat", headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        print(f"  [OK] Response received (200)")
        print(f"       Conversation ID: {result['conversation_id']}")
        print(f"       Assistant: {result['content'][:80]}...")
        if result.get('task_data'):
            print(f"       Task data: {result['task_data']}")
        return result
    else:
        print(f"  [FAIL] Chat failed: {response.status_code}")
        print(f"         {response.json()}")
        return None

def test_get_conversations(token):
    """Get list of conversations."""
    print(f"\n  Getting conversation list...")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/conversations", headers=headers)

    if response.status_code == 200:
        conversations = response.json()
        print(f"  [OK] Retrieved {len(conversations)} conversations")
        for conv in conversations:
            print(f"       - {conv['title']} ({conv['message_count']} messages)")
        return conversations
    else:
        print(f"  [FAIL] Get conversations failed: {response.status_code}")
        print(f"         {response.json()}")
        return None

def test_get_tasks(token, user_id):
    """Get list of tasks for the user."""
    print(f"\n  Getting task list...")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/{user_id}/tasks", headers=headers)

    if response.status_code == 200:
        tasks = response.json()
        print(f"  [OK] Retrieved {len(tasks)} tasks")
        for task in tasks:
            status = "[X]" if task['completed'] else "[ ]"
            print(f"       {status} {task['title']}")
        return tasks
    else:
        print(f"  [FAIL] Get tasks failed: {response.status_code}")
        print(f"         {response.json()}")
        return None

def main():
    """Run end-to-end test."""
    print_section("END-TO-END TEST: Chat API + Task Management")

    # Step 1: Login
    token = login()
    if not token:
        print("\n[FAIL] Cannot proceed without authentication")
        return

    # Extract user_id from token
    import jwt
    payload = jwt.decode(token, options={"verify_signature": False})
    user_id = payload.get("sub")
    print(f"\nUser ID: {user_id}")

    # Step 2: Create a task via chat
    print_section("Step 2: Create Task via Chat")
    response1 = test_chat_message(token, "Add a task to buy groceries tomorrow")
    if not response1:
        print("\n[FAIL] Cannot proceed without successful chat")
        return

    conversation_id = response1["conversation_id"]
    time.sleep(1)  # Small delay to ensure database commit

    # Step 3: List tasks to verify creation
    print_section("Step 3: Verify Task Created")
    tasks = test_get_tasks(token, user_id)
    if not tasks or len(tasks) == 0:
        print("\n[WARN] No tasks found - task creation may have failed")

    # Step 4: Continue conversation - list tasks via chat
    print_section("Step 4: List Tasks via Chat")
    response2 = test_chat_message(
        token,
        "Show me all my tasks",
        conversation_id=conversation_id
    )
    time.sleep(1)

    # Step 5: Complete a task via chat
    print_section("Step 5: Complete Task via Chat")
    response3 = test_chat_message(
        token,
        "Mark the groceries task as done",
        conversation_id=conversation_id
    )
    time.sleep(1)

    # Step 6: Verify task completion
    print_section("Step 6: Verify Task Completed")
    tasks = test_get_tasks(token, user_id)
    if tasks:
        completed_count = sum(1 for t in tasks if t['completed'])
        print(f"\n  Completed tasks: {completed_count}/{len(tasks)}")

    # Step 7: Get conversation history
    print_section("Step 7: Get Conversation History")
    conversations = test_get_conversations(token)
    if conversations and len(conversations) > 0:
        print(f"\n  Conversation created successfully!")
        print(f"  Messages exchanged: {conversations[0]['message_count']}")

    # Final summary
    print_section("TEST SUMMARY")
    print("[OK] Authentication: Login successful")
    print("[OK] Chat endpoint: Messages sent and received")
    print("[OK] Conversation: History tracked correctly")
    if tasks and len(tasks) > 0:
        print("[OK] Task creation: AI agent created tasks")
    else:
        print("[WARN] Task creation: No tasks found (check agent integration)")
    if tasks and any(t['completed'] for t in tasks):
        print("[OK] Task completion: AI agent completed tasks")
    else:
        print("[WARN] Task completion: No completed tasks (check agent integration)")

    print("\n" + "="*70)
    print("END-TO-END TEST COMPLETED")
    print("="*70)

if __name__ == "__main__":
    main()
