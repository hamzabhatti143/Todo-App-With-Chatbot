# Quickstart Guide: Database Models and Migrations

**Feature**: 014-database-models
**Date**: 2026-01-16

## Overview

This guide provides step-by-step instructions for setting up the database layer of the Todo Full-Stack Web Application, including environment configuration, migration management, and connection testing.

## Prerequisites

Before starting, ensure you have:

- **Python 3.11 or higher** installed
  ```bash
  python --version  # Should show 3.11+
  ```

- **PostgreSQL client tools** (optional, for manual verification)
  ```bash
  psql --version
  ```

- **Neon PostgreSQL account** (free tier available)
  - Sign up at: https://neon.tech
  - Create a new project
  - Obtain connection string

- **Project repository** cloned locally
  ```bash
  git clone <repository-url>
  cd todo-fullstack-web
  ```

## Step 1: Environment Setup

### 1.1 Navigate to Backend Directory

```bash
cd backend
```

### 1.2 Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 1.3 Install Dependencies

```bash
# Install all backend dependencies
pip install -r requirements.txt

# Verify SQLModel and Alembic are installed
pip show sqlmodel alembic psycopg2-binary
```

Expected output:
```
Name: sqlmodel
Version: 0.0.22
...

Name: alembic
Version: 1.14.0
...

Name: psycopg2-binary
Version: 2.9.10
...
```

### 1.4 Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

Required environment variables:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@ep-xxx-xxx.us-east-2.aws.neon.tech/dbname?sslmode=require

# Debug Mode (enable SQL query echoing)
DEBUG=True

# Authentication (for full application)
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000
```

**CRITICAL**: Replace the `DATABASE_URL` with your actual Neon PostgreSQL connection string. It should include:
- Username and password
- Neon host (e.g., `ep-xxx-xxx.us-east-2.aws.neon.tech`)
- Database name
- **`?sslmode=require`** parameter (mandatory for Neon)

### 1.5 Verify Neon Connection String Format

Your Neon connection string should look like:
```
postgresql://username:password@hostname.region.aws.neon.tech/database?sslmode=require
```

Example:
```
postgresql://myuser:mypass@ep-cool-cloud-123456.us-east-2.aws.neon.tech/todo_db?sslmode=require
```

## Step 2: Database Connection Testing

### 2.1 Test Connection with Python Script

Create a test script `test_connection.py`:

```python
from sqlmodel import create_engine, Session, select
from app.config import settings
from app.models import Task, Conversation, Message

# Test database connection
try:
    engine = create_engine(settings.database_url, echo=True)
    with Session(engine) as session:
        # Execute simple query
        result = session.execute(select(1))
        print("✅ Database connection successful!")
        print(f"Connected to: {settings.database_url.split('@')[1].split('/')[0]}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

Run the test:

```bash
python test_connection.py
```

Expected output:
```
✅ Database connection successful!
Connected to: ep-xxx-xxx.us-east-2.aws.neon.tech
```

### 2.2 Test with psql (Optional)

If you have PostgreSQL client tools installed:

```bash
# Extract DATABASE_URL from .env
export DATABASE_URL=$(grep DATABASE_URL .env | cut -d '=' -f2)

# Connect via psql
psql "$DATABASE_URL"
```

Once connected, verify SSL:
```sql
SHOW ssl;  -- Should show 'on'
\conninfo  -- Shows connection details including SSL
\q         -- Exit
```

## Step 3: Alembic Migration Management

### 3.1 Verify Alembic Configuration

Check that Alembic is properly configured:

```bash
# View alembic.ini
cat alembic.ini | grep sqlalchemy.url

# View current migration version (should show nothing if new database)
alembic current
```

### 3.2 Review Existing Migrations

```bash
# List all migration files
ls alembic/versions/

# View migration history
alembic history --verbose
```

Expected output:
```
<base> -> xxxxx (head), Initial schema
xxxxx -> yyyyy, Add conversations and messages tables
```

### 3.3 Apply Migrations

**IMPORTANT**: This will create tables in your Neon database.

```bash
# Apply all pending migrations
alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> xxxxx, Initial schema
INFO  [alembic.runtime.migration] Running upgrade xxxxx -> yyyyy, Add conversations and messages
```

### 3.4 Verify Migration Status

```bash
# Check current version
alembic current

# Should show:
# xxxxx (head)
```

### 3.5 Verify Tables Created

Using Python:

```python
from sqlmodel import create_engine, text
from app.config import settings

engine = create_engine(settings.database_url)
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """))
    tables = [row[0] for row in result]
    print("Created tables:")
    for table in tables:
        print(f"  - {table}")
```

Expected output:
```
Created tables:
  - alembic_version
  - conversations
  - messages
  - tasks
  - users
```

## Step 4: Testing Database Operations

### 4.1 Create Test Script

Create `test_models.py`:

```python
from sqlmodel import Session, select
from datetime import datetime
from uuid import uuid4

from app.database import engine
from app.models import User, Task, Conversation, Message, MessageRole

def test_database_operations():
    with Session(engine) as session:
        # 1. Create test user
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_here"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"✅ Created user: {user.id}")

        # 2. Create test task
        task = Task(
            user_id=user.id,
            title="Test Task",
            description="This is a test task"
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        print(f"✅ Created task: {task.title}")

        # 3. Create conversation
        conversation = Conversation(user_id=user.id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        print(f"✅ Created conversation: {conversation.id}")

        # 4. Create messages
        message1 = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content="Hello, AI assistant!"
        )
        message2 = Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content="Hello! How can I help you today?"
        )
        session.add_all([message1, message2])
        session.commit()
        print(f"✅ Created {2} messages")

        # 5. Query data
        tasks = session.exec(select(Task).where(Task.user_id == user.id)).all()
        print(f"✅ Retrieved {len(tasks)} task(s)")

        messages = session.exec(
            select(Message).where(Message.conversation_id == conversation.id)
        ).all()
        print(f"✅ Retrieved {len(messages)} message(s)")

        # 6. Test cascade deletion
        session.delete(conversation)
        session.commit()
        remaining_messages = session.exec(
            select(Message).where(Message.conversation_id == conversation.id)
        ).all()
        assert len(remaining_messages) == 0
        print(f"✅ Cascade deletion verified (messages deleted with conversation)")

        # 7. Cleanup
        session.delete(task)
        session.delete(user)
        session.commit()
        print("✅ Cleanup complete")

if __name__ == "__main__":
    test_database_operations()
    print("\n🎉 All database operations completed successfully!")
```

Run the test:

```bash
python test_models.py
```

Expected output:
```
✅ Created user: <uuid>
✅ Created task: Test Task
✅ Created conversation: <uuid>
✅ Created 2 messages
✅ Retrieved 1 task(s)
✅ Retrieved 2 message(s)
✅ Cascade deletion verified (messages deleted with conversation)
✅ Cleanup complete

🎉 All database operations completed successfully!
```

### 4.2 Verify Indexes

Check that indexes are being used:

```python
from sqlmodel import create_engine, text
from app.config import settings

engine = create_engine(settings.database_url)
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT
            tablename,
            indexname,
            indexdef
        FROM pg_indexes
        WHERE schemaname = 'public'
        ORDER BY tablename, indexname;
    """))

    print("Database indexes:")
    for row in result:
        print(f"  {row[0]}.{row[1]}")
```

Expected output:
```
Database indexes:
  tasks.ix_tasks_user_id
  tasks.ix_tasks_title
  conversations.ix_conversations_user_id
  messages.ix_messages_conversation_id
  users.ix_users_email
```

## Step 5: Creating New Migrations

### 5.1 Modify a Model

Example: Add a `priority` field to Task model:

```python
# app/models/task.py
class Task(SQLModel, table=True):
    # ... existing fields ...
    priority: int = Field(default=0)  # New field
```

### 5.2 Generate Migration

```bash
# Generate migration automatically
alembic revision --autogenerate -m "Add priority field to tasks"
```

Alembic will create a new file in `alembic/versions/` like `xxxxx_add_priority_field_to_tasks.py`.

### 5.3 Review Generated Migration

```bash
# Open the generated migration file
nano alembic/versions/xxxxx_add_priority_field_to_tasks.py
```

Verify the `upgrade()` and `downgrade()` functions:

```python
def upgrade() -> None:
    op.add_column('tasks', sa.Column('priority', sa.Integer(), nullable=False, server_default='0'))

def downgrade() -> None:
    op.drop_column('tasks', 'priority')
```

### 5.4 Apply New Migration

```bash
alembic upgrade head
```

### 5.5 Rollback if Needed

```bash
# Rollback last migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>

# Rollback all migrations
alembic downgrade base
```

## Step 6: Common Operations

### Start FastAPI Application

```bash
# From backend/ directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/docs to see Swagger API documentation.

### Check Migration History

```bash
# Show all migrations
alembic history

# Show current version
alembic current

# Show pending migrations
alembic heads
```

### Generate Migration Without Autogenerate

For complex changes that autogenerate might miss:

```bash
alembic revision -m "Manual migration description"
```

Then edit the generated file manually.

## Troubleshooting

### Error: `psycopg2.OperationalError: SSL connection required`

**Solution**: Add `?sslmode=require` to your `DATABASE_URL`:
```env
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
```

### Error: `alembic.util.exc.CommandError: Target database is not up to date`

**Solution**: Run pending migrations:
```bash
alembic upgrade head
```

### Error: `sqlalchemy.exc.ProgrammingError: relation "tasks" does not exist`

**Solution**: Run migrations to create tables:
```bash
alembic upgrade head
```

### Error: `ModuleNotFoundError: No module named 'app'`

**Solution**: Ensure you're in the `backend/` directory and virtual environment is activated:
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### Error: `pydantic_core._pydantic_core.ValidationError: database_url`

**Solution**: Verify `.env` file exists and contains valid `DATABASE_URL`:
```bash
cat .env | grep DATABASE_URL
```

### Slow Query Performance

**Debug**: Enable query logging and use EXPLAIN ANALYZE:
```python
# In .env
DEBUG=True

# In Python
from sqlmodel import text
result = conn.execute(text("EXPLAIN ANALYZE SELECT * FROM tasks WHERE user_id = 'uuid'"))
print(result.fetchall())
```

Look for "Seq Scan" instead of "Index Scan" - if found, check that indexes exist.

## Best Practices

### 1. Always Review Autogenerated Migrations

Alembic's autogenerate is helpful but not perfect. Always review generated migrations before applying.

### 2. Test Migrations on Development First

Never run untested migrations directly on production:
```bash
# Test upgrade
alembic upgrade head

# Test downgrade
alembic downgrade -1

# Re-apply
alembic upgrade head
```

### 3. Use Transactions for Data Migrations

When modifying data during migrations:
```python
from alembic import op
from sqlalchemy import text

def upgrade():
    connection = op.get_bind()
    connection.execute(text("UPDATE tasks SET priority = 0 WHERE priority IS NULL"))
```

### 4. Keep Migrations Small and Focused

One logical change per migration (easier to review, test, and rollback).

### 5. Never Edit Applied Migrations

Once a migration is applied (especially in production), never edit it. Create a new migration instead.

### 6. Backup Before Major Changes

Before running migrations on production:
```bash
# Create Neon backup via dashboard
# Or export via pg_dump
```

## Additional Resources

- **SQLModel Documentation**: https://sqlmodel.tiangolo.com/
- **Alembic Tutorial**: https://alembic.sqlalchemy.org/en/latest/tutorial.html
- **Neon Documentation**: https://neon.tech/docs/
- **PostgreSQL Data Types**: https://www.postgresql.org/docs/current/datatype.html
- **FastAPI Database Guide**: https://fastapi.tiangolo.com/tutorial/sql-databases/

## Next Steps

After completing this setup:

1. **Run Tests**: Execute backend tests to verify all models work correctly
   ```bash
   pytest
   ```

2. **Start Development**: Begin implementing API endpoints that use these models
   - See `backend/app/routes/` for example endpoints
   - Reference constitution at `.specify/memory/constitution.md` for coding standards

3. **Frontend Integration**: Connect frontend to backend API
   - Frontend located in `frontend/` directory
   - API base URL: `http://localhost:8000`

4. **Documentation**: Update documentation as schema evolves
   - Document schema changes in commit messages
   - Update this quickstart if workflow changes

---

**Congratulations!** 🎉 You've successfully set up the database layer for the Todo Full-Stack Web Application. You can now create, read, update, and delete tasks and conversations with full type safety and migration support.
