"""
Pytest configuration and fixtures for backend tests.

Provides test fixtures for database sessions, test client, and authentication.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from uuid import uuid4

from app.main import app
from app.database import get_session
from app.dependencies import get_current_user
from app.models.user import User
from app.auth import get_password_hash


@pytest.fixture(name="session")
def session_fixture():
    """
    Create in-memory SQLite database for testing.

    Yields:
        Session: SQLModel database session with test data
    """
    # Create in-memory SQLite engine
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create all tables
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    """
    Create a test user in the database.

    Args:
        session: Database session

    Returns:
        User: Test user instance
    """
    user = User(
        id=uuid4(),
        email="test@example.com",
        hashed_password=get_password_hash("testpassword123"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="other_user")
def other_user_fixture(session: Session):
    """
    Create another test user for testing user isolation.

    Args:
        session: Database session

    Returns:
        User: Another test user instance
    """
    user = User(
        id=uuid4(),
        email="other@example.com",
        hashed_password=get_password_hash("otherpassword123"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="client")
def client_fixture(session: Session, test_user: User):
    """
    Create test client with overridden database session and authentication.

    Args:
        session: Database session fixture
        test_user: Test user fixture

    Returns:
        TestClient: FastAPI test client
    """
    # Import here to avoid circular imports
    from app.main import app as fastapi_app

    def get_session_override():
        return session

    def get_current_user_override():
        return test_user

    # Override dependencies
    fastapi_app.dependency_overrides[get_session] = get_session_override
    fastapi_app.dependency_overrides[get_current_user] = get_current_user_override

    client = TestClient(fastapi_app)
    yield client

    # Clear overrides after test
    fastapi_app.dependency_overrides.clear()


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(test_user: User):
    """
    Create authorization headers with JWT token for test user.

    Args:
        test_user: Test user fixture

    Returns:
        dict: Authorization headers with Bearer token
    """
    from app.auth import create_access_token

    token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}
