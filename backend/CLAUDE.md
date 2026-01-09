# Backend Development Guidelines

This file provides guidance for AI assistants working on the FastAPI backend.

## Architecture Principles

1. **API-First Design**: RESTful API with clear endpoint structure
2. **Type Safety**: Use SQLModel for type-safe database operations and Pydantic for validation
3. **Separation of Concerns**: Models, routes, and schemas in separate modules
4. **Security First**: Authentication, authorization, input validation, and SQL injection prevention

## Code Standards

### Python Style
- Follow PEP 8 style guide
- Use type hints for all function parameters and return values
- Maximum line length: 100 characters
- Use docstrings for modules, classes, and functions

### Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app and middleware
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py          # Task database model
│   │   └── user.py          # User database model
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── tasks.py         # Task endpoints
│   │   └── auth.py          # Authentication endpoints
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py          # Task Pydantic schemas
│   │   └── user.py          # User Pydantic schemas
│   ├── database.py          # Database connection and session
│   ├── auth.py              # Authentication utilities
│   └── dependencies.py      # FastAPI dependencies
├── alembic/
│   ├── versions/            # Migration files
│   └── env.py               # Alembic configuration
└── tests/
    ├── conftest.py          # Pytest fixtures
    ├── test_tasks.py        # Task endpoint tests
    └── test_auth.py         # Auth endpoint tests
```

### Database Models (SQLModel)

Use SQLModel for database models with proper type hints:

```python
# app/models/task.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class Task(SQLModel, table=True):
    """Task database model"""
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=200, index=True)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Pydantic Schemas

Separate schemas for request/response validation:

```python
# app/schemas/task.py
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional

class TaskBase(BaseModel):
    """Base task schema"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class TaskCreate(TaskBase):
    """Schema for creating a task"""
    pass

class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None

class TaskResponse(TaskBase):
    """Schema for task response"""
    id: UUID
    completed: bool
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### API Routes

Use FastAPI router pattern with dependency injection:

```python
# app/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from uuid import UUID
from typing import List

from app.database import get_session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(
    user_id: UUID,
    session: Session = Depends(get_session),
    current_user: UUID = Depends(get_current_user)
):
    """Get all tasks for a user"""
    if current_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks

@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: UUID,
    task: TaskCreate,
    session: Session = Depends(get_session),
    current_user: UUID = Depends(get_current_user)
):
    """Create a new task"""
    if current_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    db_task = Task(**task.dict(), user_id=user_id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

### Database Connection

```python
# app/database.py
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency for database sessions"""
    with Session(engine) as session:
        yield session
```

### Authentication

Use JWT tokens with dependency injection:

```python
# app/auth.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
```

```python
# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID

from app.auth import decode_token

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UUID:
    """Get current user from JWT token"""
    token = credentials.credentials
    payload = decode_token(token)
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    return UUID(user_id)
```

## Error Handling

Use FastAPI's HTTPException for consistent error responses:

```python
from fastapi import HTTPException, status

# 400 Bad Request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid input data"
)

# 401 Unauthorized
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

# 403 Forbidden
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not authorized to access this resource"
)

# 404 Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Task not found"
)

# 500 Internal Server Error (catch unexpected errors)
try:
    # database operation
except Exception as e:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error"
    )
```

## Testing

Use pytest with FastAPI's TestClient:

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from app.main import app
from app.database import get_session

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

```python
# tests/test_tasks.py
def test_create_task(client):
    response = client.post(
        "/api/user-id/tasks",
        json={"title": "Test Task", "description": "Test Description"},
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["completed"] is False
```

## Database Migrations with Alembic

Always use migrations for schema changes:

```bash
# Create migration after model changes
alembic revision --autogenerate -m "Add tasks table"

# Review the generated migration file
# Edit if needed, then apply
alembic upgrade head
```

## Security Checklist

- [ ] All passwords are hashed with bcrypt
- [ ] JWT tokens are used for authentication
- [ ] Tokens expire after configured time
- [ ] User authorization checks on all endpoints
- [ ] Input validation with Pydantic schemas
- [ ] SQL injection protection via SQLModel/SQLAlchemy
- [ ] CORS configured for specific origins only
- [ ] Secrets stored in environment variables, not code
- [ ] HTTPS enforced in production
- [ ] Rate limiting configured (if needed)

## Performance Considerations

- Use database indexes on frequently queried fields
- Implement pagination for list endpoints
- Use async/await for I/O operations
- Connection pooling for database
- Cache frequent queries if needed

## Database Session Management

### Session Dependency

Use FastAPI's dependency injection for database sessions:

```python
# app/database.py
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    """Dependency for database sessions"""
    with Session(engine) as session:
        yield session
```

### Using Sessions in Routes

```python
from app.database import get_session
from sqlmodel import Session

@router.get("/items")
async def get_items(session: Session = Depends(get_session)):
    statement = select(Item)
    items = session.exec(statement).all()
    return items
```

**Best Practices**:
- Always use dependency injection for sessions
- Never create sessions manually in route handlers
- Sessions are automatically closed after request
- Use `session.commit()` to persist changes
- Use `session.refresh(obj)` to reload object after commit

## User Isolation Patterns

### Mandatory Authorization Check

Every endpoint accessing user data MUST verify user ownership:

```python
@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(
    user_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get all tasks for authenticated user"""

    # CRITICAL: Verify user_id matches authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    # Query with user_id filter
    statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    tasks = session.exec(statement).all()
    return tasks
```

**Security Principle**: Always filter by `user_id` extracted from JWT token, never trust URL parameters alone.

### Task Ownership Verification

When accessing specific tasks, verify both task existence and ownership:

```python
@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: UUID,
    task_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get a specific task"""

    # Verify user authorization
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    # Query task with both user_id and task_id filters
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # Ownership verification
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )

    return task
```

## JWT Authentication Implementation

### Token Creation

```python
# app/auth.py
from datetime import datetime, timedelta
from jose import jwt
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token with user_id in payload"""
    to_encode = data.copy()

    # Set expiration
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    # Encode token with secret key
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### Token Verification

```python
# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlmodel import Session, select
from uuid import UUID

from app.auth import decode_token
from app.database import get_session
from app.models.user import User

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """Extract and verify user from JWT token"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode and verify token
        token = credentials.credentials
        payload = decode_token(token)

        # Extract user_id from 'sub' claim
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Verify user exists in database
    user_uuid = UUID(user_id)
    statement = select(User).where(User.id == user_uuid)
    user = session.exec(statement).first()

    if user is None:
        raise credentials_exception

    return user
```

### Using Authentication in Routes

```python
from app.dependencies import get_current_user
from app.models.user import User

@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: UUID,
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)  # Requires JWT authentication
):
    """Create a new task (protected endpoint)"""

    # Verify authorization
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    # Create task
    db_task = Task(**task_data.model_dump(), user_id=user_id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task
```

## Database Migrations with Alembic

### Creating Migrations

```bash
# After modifying SQLModel models, generate migration
alembic revision --autogenerate -m "Add new field to tasks table"

# Review generated migration in alembic/versions/
# Edit if necessary, then apply
alembic upgrade head
```

### Migration Best Practices

1. **Always review auto-generated migrations** - Alembic might miss some changes
2. **Test migrations on development data first**
3. **Include both upgrade and downgrade functions**
4. **Add data migrations when changing schema**
5. **Backup production database before migrating**

### Common Migration Patterns

#### Adding a Column

```python
# alembic/versions/xxx_add_priority_to_tasks.py
def upgrade():
    op.add_column('tasks', sa.Column('priority', sa.Integer(), nullable=True))

def downgrade():
    op.drop_column('tasks', 'priority')
```

#### Adding an Index

```python
def upgrade():
    op.create_index('idx_tasks_priority', 'tasks', ['priority'])

def downgrade():
    op.drop_index('idx_tasks_priority', table_name='tasks')
```

#### Data Migration

```python
from sqlalchemy import text

def upgrade():
    # Add column first
    op.add_column('tasks', sa.Column('priority', sa.Integer(), nullable=True))

    # Populate existing rows
    connection = op.get_bind()
    connection.execute(text("UPDATE tasks SET priority = 0 WHERE priority IS NULL"))

    # Make column non-nullable
    op.alter_column('tasks', 'priority', nullable=False)

def downgrade():
    op.drop_column('tasks', 'priority')
```

## CORS Configuration

### Environment-Based CORS

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="Todo API",
    description="RESTful API for todo task management",
    version="1.0.0"
)

# Parse allowed origins from environment variable
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Whitelist only, never "*" in production
    allow_credentials=True,  # Allow cookies and auth headers
    allow_methods=["*"],     # Allow all HTTP methods
    allow_headers=["*"],     # Allow all headers
)
```

**Security Note**: Never use `allow_origins=["*"]` in production with `allow_credentials=True`.

## Testing Patterns

### Test Setup with SQLite

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from app.main import app
from app.database import get_session

@pytest.fixture(name="session")
def session_fixture():
    """Create in-memory SQLite database for testing"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test client with overridden session"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

### Testing Protected Endpoints

```python
# tests/test_tasks.py
import pytest
from app.auth import create_access_token

@pytest.fixture
def auth_headers(test_user):
    """Create authorization headers with JWT token"""
    token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}

def test_create_task(client, test_user, auth_headers):
    """Test creating a task with authentication"""
    response = client.post(
        f"/api/{test_user.id}/tasks",
        json={"title": "Test Task", "description": "Test Description"},
        headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["user_id"] == str(test_user.id)
```

### Testing User Isolation

```python
def test_cannot_access_other_user_tasks(client, test_user, other_user, auth_headers):
    """Verify users cannot access other users' tasks"""
    response = client.get(
        f"/api/{other_user.id}/tasks",  # Trying to access other user's tasks
        headers=auth_headers  # With test_user's token
    )

    assert response.status_code == 403
    assert "Not authorized" in response.json()["detail"]
```

## Environment Variables Best Practices

### Required Variables

```python
# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database
    database_url: str

    # Authentication
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: str = "http://localhost:3000"

    # Application
    debug: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False

# Create global settings instance
settings = Settings()
```

### Using Settings

```python
from app.config import settings

# In database.py
engine = create_engine(settings.database_url)

# In auth.py
SECRET_KEY = settings.jwt_secret_key

# In main.py
origins = settings.cors_origins.split(",")
```

## Common Patterns

### Updating Timestamps

```python
from datetime import datetime

@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: UUID,
    task_id: UUID,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update a task"""

    # Verify authorization and get task
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update fields
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task
```

### Pagination Pattern

```python
from typing import Optional

@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(
    user_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get tasks with pagination"""

    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    tasks = session.exec(statement).all()
    return tasks
```

## Error Logging

### Structured Logging

```python
import logging
from fastapi import Request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch all unhandled exceptions"""
    logger.error(
        f"Unhandled exception: {exc}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "client": request.client.host
        }
    )

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

## Performance Optimization

### Database Connection Pooling

```python
from sqlmodel import create_engine

# Configure connection pool
engine = create_engine(
    DATABASE_URL,
    echo=settings.debug,
    pool_size=20,           # Maximum number of connections
    max_overflow=10,        # Additional connections allowed
    pool_pre_ping=True,     # Verify connection health before use
    pool_recycle=3600,      # Recycle connections after 1 hour
)
```

### Query Optimization

```python
# Bad: N+1 query problem
tasks = session.exec(select(Task)).all()
for task in tasks:
    user = session.exec(select(User).where(User.id == task.user_id)).first()

# Good: Join to fetch related data in single query
from sqlmodel import select

statement = (
    select(Task, User)
    .join(User, Task.user_id == User.id)
    .where(User.id == user_id)
)
results = session.exec(statement).all()
```

## Dependencies

Refer to requirements.txt for current versions. Key dependencies:
- fastapi: 0.115.6
- sqlmodel: 0.0.22
- uvicorn: 0.34.0
- python-jose: 3.3.0
- passlib: 1.7.4
- alembic: 1.14.0
- pydantic: 2.10.4
- psycopg2-binary: 2.9.10
- pytest: 8.3.4

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
