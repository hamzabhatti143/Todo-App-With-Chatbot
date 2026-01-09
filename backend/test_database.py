"""
Test Database Connection and Models

This script tests the database models using SQLite in-memory database.
"""

from sqlmodel import SQLModel, create_engine, Session, select
from app.models.user import User
from app.models.task import Task
from datetime import datetime
import uuid

# Create SQLite in-memory engine for testing
test_engine = create_engine("sqlite:///:memory:", echo=True)


def test_models():
    """Test database models"""
    print("\n" + "="*60)
    print("Testing Database Models")
    print("="*60)

    # Create tables
    print("\n1. Creating database tables...")
    SQLModel.metadata.create_all(test_engine)
    print("✓ Tables created successfully")

    # Test User model
    print("\n2. Testing User model...")
    with Session(test_engine) as session:
        # Create user
        test_user = User(
            email="test@example.com",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU8.cH9h7bTu"
        )
        session.add(test_user)
        session.commit()
        session.refresh(test_user)
        print(f"✓ User created: {test_user.email} (ID: {test_user.id})")

        # Query user
        statement = select(User).where(User.email == "test@example.com")
        user = session.exec(statement).first()
        assert user is not None
        assert user.email == "test@example.com"
        print("✓ User query successful")

        user_id = user.id

    # Test Task model
    print("\n3. Testing Task model...")
    with Session(test_engine) as session:
        # Get user
        user = session.get(User, user_id)

        # Create tasks
        task1 = Task(
            title="Complete project documentation",
            description="Write comprehensive README and API docs",
            user_id=user.id,
            completed=False
        )
        task2 = Task(
            title="Implement authentication",
            description="Add JWT-based authentication",
            user_id=user.id,
            completed=True
        )
        session.add(task1)
        session.add(task2)
        session.commit()
        session.refresh(task1)
        session.refresh(task2)
        print(f"✓ Task 1 created: {task1.title} (Completed: {task1.completed})")
        print(f"✓ Task 2 created: {task2.title} (Completed: {task2.completed})")

        # Query all tasks for user
        statement = select(Task).where(Task.user_id == user.id)
        tasks = session.exec(statement).all()
        print(f"✓ Found {len(tasks)} tasks for user")

        # Query completed tasks
        statement = select(Task).where(Task.user_id == user.id, Task.completed == True)
        completed_tasks = session.exec(statement).all()
        print(f"✓ Found {len(completed_tasks)} completed tasks")

        # Query incomplete tasks
        statement = select(Task).where(Task.user_id == user.id, Task.completed == False)
        incomplete_tasks = session.exec(statement).all()
        print(f"✓ Found {len(incomplete_tasks)} incomplete tasks")

        # Update task
        task1.completed = True
        task1.updated_at = datetime.utcnow()
        session.add(task1)
        session.commit()
        session.refresh(task1)
        print(f"✓ Task 1 updated: completed={task1.completed}")

        # Delete task
        session.delete(task2)
        session.commit()
        print("✓ Task 2 deleted")

        # Verify deletion
        statement = select(Task).where(Task.user_id == user.id)
        remaining_tasks = session.exec(statement).all()
        assert len(remaining_tasks) == 1
        print(f"✓ Verified: {len(remaining_tasks)} task remaining")

    # Test schema validation
    print("\n4. Testing Pydantic schemas...")
    from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
    from app.schemas.user import UserCreate, UserLogin, UserResponse

    # Test TaskCreate
    task_create = TaskCreate(title="Test task", description="Test description")
    assert task_create.title == "Test task"
    print("✓ TaskCreate schema validated")

    # Test TaskUpdate
    task_update = TaskUpdate(completed=True)
    assert task_update.completed == True
    print("✓ TaskUpdate schema validated")

    # Test UserCreate
    user_create = UserCreate(email="newuser@example.com", password="password123")
    assert user_create.email == "newuser@example.com"
    print("✓ UserCreate schema validated")

    # Test UserLogin
    user_login = UserLogin(email="user@example.com", password="password")
    assert user_login.email == "user@example.com"
    print("✓ UserLogin schema validated")

    print("\n" + "="*60)
    print("All tests passed successfully! ✓")
    print("="*60)


if __name__ == "__main__":
    try:
        test_models()
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
