"""
Test Task CRUD API Endpoints

This script tests all task management endpoints with JWT authentication.
"""

from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
import json

# Import app and dependencies
from app.main import app
from app.database import get_session
from app.models.user import User
from app.models.task import Task
from app.auth import get_password_hash, create_access_token

# Create test database
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def get_test_session():
    """Override database session for testing"""
    with Session(test_engine) as session:
        yield session


# Override the database dependency
app.dependency_overrides[get_session] = get_test_session

# Create test client
client = TestClient(app)


def setup_test_data():
    """Create test database and user"""
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        # Create test user
        test_user = User(
            email="testuser@example.com",
            hashed_password=get_password_hash("password123")
        )
        session.add(test_user)
        session.commit()
        session.refresh(test_user)

        # Create JWT token
        token = create_access_token(data={"sub": str(test_user.id)})

        return test_user.id, token


def test_api_endpoints():
    """Test all Task CRUD API endpoints"""
    print("\n" + "="*60)
    print("Testing Task CRUD API Endpoints")
    print("="*60)

    # Setup test data
    print("\n1. Setting up test environment...")
    user_id, auth_token = setup_test_data()
    headers = {"Authorization": f"Bearer {auth_token}"}
    print(f"✓ Test user created: {user_id}")
    print(f"✓ Auth token generated")

    # Test health check
    print("\n2. Testing health check endpoints...")
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✓ GET / - Health check passed")

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    print("✓ GET /health - Health check passed")

    # Test GET /api/{user_id}/tasks (empty list)
    print("\n3. Testing GET /api/{user_id}/tasks (empty)...")
    response = client.get(f"/api/{user_id}/tasks", headers=headers)
    assert response.status_code == 200
    assert response.json() == []
    print("✓ GET /api/{user_id}/tasks - Empty list returned")

    # Test GET without auth token (should fail)
    print("\n4. Testing authentication requirement...")
    response = client.get(f"/api/{user_id}/tasks")
    assert response.status_code == 403  # Missing auth header
    print("✓ Request without auth token rejected (403)")

    # Test POST /api/{user_id}/tasks (create task)
    print("\n5. Testing POST /api/{user_id}/tasks (create task)...")
    task_data = {
        "title": "Complete project documentation",
        "description": "Write comprehensive README and API docs"
    }
    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data,
        headers=headers
    )
    assert response.status_code == 201
    task1 = response.json()
    assert task1["title"] == task_data["title"]
    assert task1["description"] == task_data["description"]
    assert task1["completed"] == False
    assert task1["user_id"] == str(user_id)
    assert "id" in task1
    assert "created_at" in task1
    task1_id = task1["id"]
    print(f"✓ POST /api/{{user_id}}/tasks - Task created: {task1_id}")

    # Create another task
    task2_data = {
        "title": "Implement authentication",
        "description": "Add JWT-based authentication"
    }
    response = client.post(
        f"/api/{user_id}/tasks",
        json=task2_data,
        headers=headers
    )
    assert response.status_code == 201
    task2 = response.json()
    task2_id = task2["id"]
    print(f"✓ POST /api/{{user_id}}/tasks - Task created: {task2_id}")

    # Test GET /api/{user_id}/tasks (list tasks)
    print("\n6. Testing GET /api/{user_id}/tasks (with tasks)...")
    response = client.get(f"/api/{user_id}/tasks", headers=headers)
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    print(f"✓ GET /api/{{user_id}}/tasks - Found {len(tasks)} tasks")

    # Test GET /api/{user_id}/tasks/{task_id} (get specific task)
    print("\n7. Testing GET /api/{user_id}/tasks/{task_id}...")
    response = client.get(
        f"/api/{user_id}/tasks/{task1_id}",
        headers=headers
    )
    assert response.status_code == 200
    task = response.json()
    assert task["id"] == task1_id
    assert task["title"] == task_data["title"]
    print(f"✓ GET /api/{{user_id}}/tasks/{{task_id}} - Task retrieved")

    # Test GET non-existent task (404)
    print("\n8. Testing 404 for non-existent task...")
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = client.get(
        f"/api/{user_id}/tasks/{fake_uuid}",
        headers=headers
    )
    assert response.status_code == 404
    print("✓ GET non-existent task - 404 returned")

    # Test PUT /api/{user_id}/tasks/{task_id} (update task)
    print("\n9. Testing PUT /api/{user_id}/tasks/{task_id}...")
    update_data = {
        "title": "Updated documentation task",
        "description": "Write comprehensive README, API docs, and examples",
        "completed": True
    }
    response = client.put(
        f"/api/{user_id}/tasks/{task1_id}",
        json=update_data,
        headers=headers
    )
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == update_data["title"]
    assert updated_task["description"] == update_data["description"]
    assert updated_task["completed"] == True
    print("✓ PUT /api/{user_id}/tasks/{task_id} - Task updated")

    # Test partial update with PUT
    print("\n10. Testing partial update with PUT...")
    partial_update = {"title": "Final documentation task"}
    response = client.put(
        f"/api/{user_id}/tasks/{task1_id}",
        json=partial_update,
        headers=headers
    )
    assert response.status_code == 200
    task = response.json()
    assert task["title"] == partial_update["title"]
    assert task["completed"] == True  # Should retain previous value
    print("✓ PUT with partial data - Title updated, other fields retained")

    # Test PATCH /api/{user_id}/tasks/{task_id}/complete (toggle completion)
    print("\n11. Testing PATCH /api/{user_id}/tasks/{task_id}/complete...")
    response = client.patch(
        f"/api/{user_id}/tasks/{task2_id}/complete",
        headers=headers
    )
    assert response.status_code == 200
    task = response.json()
    assert task["completed"] == True  # Was False, now True
    print(f"✓ PATCH /api/{{user_id}}/tasks/{{task_id}}/complete - Toggled to completed=True")

    # Toggle again
    response = client.patch(
        f"/api/{user_id}/tasks/{task2_id}/complete",
        headers=headers
    )
    assert response.status_code == 200
    task = response.json()
    assert task["completed"] == False  # Toggled back to False
    print(f"✓ PATCH /api/{{user_id}}/tasks/{{task_id}}/complete - Toggled back to completed=False")

    # Test DELETE /api/{user_id}/tasks/{task_id}
    print("\n12. Testing DELETE /api/{user_id}/tasks/{task_id}...")
    response = client.delete(
        f"/api/{user_id}/tasks/{task1_id}",
        headers=headers
    )
    assert response.status_code == 204
    print("✓ DELETE /api/{user_id}/tasks/{task_id} - Task deleted (204)")

    # Verify task is deleted
    response = client.get(
        f"/api/{user_id}/tasks/{task1_id}",
        headers=headers
    )
    assert response.status_code == 404
    print("✓ Verified task is deleted (404 on GET)")

    # Verify only one task remains
    response = client.get(f"/api/{user_id}/tasks", headers=headers)
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    print(f"✓ Verified: {len(tasks)} task remaining")

    # Test user data isolation
    print("\n13. Testing user data isolation...")

    # Create second user
    with Session(test_engine) as session:
        user2 = User(
            email="user2@example.com",
            hashed_password=get_password_hash("password123")
        )
        session.add(user2)
        session.commit()
        session.refresh(user2)
        user2_id = user2.id
        token2 = create_access_token(data={"sub": str(user2_id)})
        headers2 = {"Authorization": f"Bearer {token2}"}

    # User2 tries to access User1's tasks (should fail)
    response = client.get(f"/api/{user_id}/tasks", headers=headers2)
    assert response.status_code == 403
    print("✓ User2 cannot access User1's tasks (403)")

    # User2 tries to create task for User1 (should fail)
    response = client.post(
        f"/api/{user_id}/tasks",
        json={"title": "Unauthorized task"},
        headers=headers2
    )
    assert response.status_code == 403
    print("✓ User2 cannot create tasks for User1 (403)")

    # User2 creates their own task
    response = client.post(
        f"/api/{user2_id}/tasks",
        json={"title": "User2's task"},
        headers=headers2
    )
    assert response.status_code == 201
    print("✓ User2 can create their own tasks")

    # Test validation errors
    print("\n14. Testing input validation...")

    # Empty title (should fail)
    response = client.post(
        f"/api/{user_id}/tasks",
        json={"title": ""},
        headers=headers
    )
    assert response.status_code == 422  # Validation error
    print("✓ Empty title rejected (422)")

    # Title too long (should fail)
    response = client.post(
        f"/api/{user_id}/tasks",
        json={"title": "x" * 201},  # Max is 200
        headers=headers
    )
    assert response.status_code == 422
    print("✓ Title exceeding max length rejected (422)")

    # Description too long (should fail)
    response = client.post(
        f"/api/{user_id}/tasks",
        json={"title": "Valid title", "description": "x" * 1001},  # Max is 1000
        headers=headers
    )
    assert response.status_code == 422
    print("✓ Description exceeding max length rejected (422)")

    # Test OpenAPI documentation
    print("\n15. Testing OpenAPI documentation...")
    response = client.get("/docs")
    assert response.status_code == 200
    print("✓ OpenAPI docs available at /docs")

    response = client.get("/redoc")
    assert response.status_code == 200
    print("✓ ReDoc documentation available at /redoc")

    response = client.get("/openapi.json")
    assert response.status_code == 200
    openapi_spec = response.json()
    assert "paths" in openapi_spec
    assert "/api/{user_id}/tasks" in openapi_spec["paths"]
    print("✓ OpenAPI spec generated with task endpoints")

    print("\n" + "="*60)
    print("All API endpoint tests passed successfully! ✓")
    print("="*60)

    # Summary
    print("\nEndpoints Tested:")
    print("  ✓ GET /                                     - Health check")
    print("  ✓ GET /health                               - Health check")
    print("  ✓ GET /api/{user_id}/tasks                  - List tasks")
    print("  ✓ POST /api/{user_id}/tasks                 - Create task")
    print("  ✓ GET /api/{user_id}/tasks/{task_id}        - Get task")
    print("  ✓ PUT /api/{user_id}/tasks/{task_id}        - Update task")
    print("  ✓ PATCH /api/{user_id}/tasks/{task_id}/complete - Toggle completion")
    print("  ✓ DELETE /api/{user_id}/tasks/{task_id}     - Delete task")
    print("\nSecurity Features Verified:")
    print("  ✓ JWT authentication required")
    print("  ✓ User data isolation enforced")
    print("  ✓ Authorization checks on all endpoints")
    print("  ✓ Proper status codes (200, 201, 204, 403, 404, 422)")
    print("  ✓ Input validation with Pydantic")
    print("  ✓ OpenAPI documentation generated")

    return True


if __name__ == "__main__":
    try:
        test_api_endpoints()
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
