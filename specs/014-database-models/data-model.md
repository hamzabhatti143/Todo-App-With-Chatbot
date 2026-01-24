# Data Model: Database Entities and Relationships

**Feature**: 014-database-models
**Date**: 2026-01-16
**Status**: Implemented

## Overview

This document defines the data model for the Todo Full-Stack Web Application, including three core entities (Task, Conversation, Message) with their attributes, relationships, constraints, and indexes. The model supports multi-user task management with AI-powered conversational assistance.

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User                                     │
│  ─────────────────────────────────────────────────────────────  │
│   id: UUID (PK)                                                  │
│   email: VARCHAR(255) UNIQUE NOT NULL                            │
│   hashed_password: VARCHAR(255) NOT NULL                         │
│   created_at: TIMESTAMP NOT NULL                                 │
└──────────────────┬──────────────────────────────┬────────────────┘
                   │                              │
                   │ 1                            │ 1
                   │                              │
                   │ N                            │ N
      ┌────────────▼────────────┐    ┌───────────▼────────────┐
      │         Task            │    │      Conversation       │
      │  ───────────────────    │    │  ──────────────────     │
      │  id: UUID (PK)          │    │  id: UUID (PK)          │
      │  user_id: UUID (FK)     │    │  user_id: UUID (FK)     │
      │  title: VARCHAR(200)    │    │  created_at: TIMESTAMP  │
      │  description: VARCHAR   │    │  updated_at: TIMESTAMP  │
      │  completed: BOOLEAN     │    └───────────┬─────────────┘
      │  created_at: TIMESTAMP  │                │ 1
      │  updated_at: TIMESTAMP  │                │
      └─────────────────────────┘                │ N
                                      ┌──────────▼──────────────┐
                                      │        Message          │
                                      │  ──────────────────     │
                                      │  id: UUID (PK)          │
                                      │  conversation_id: UUID  │
                                      │  role: ENUM(user,       │
                                      │            assistant)   │
                                      │  content: TEXT          │
                                      │  created_at: TIMESTAMP  │
                                      └─────────────────────────┘

Relationships:
- User → Task: One-to-Many (one user has many tasks)
- User → Conversation: One-to-Many (one user has many conversations)
- Conversation → Message: One-to-Many with CASCADE DELETE
                          (one conversation has many messages)
```

## Entity Definitions

### 1. Task

**Purpose**: Represents a user's todo item with title, description, completion status, and ownership tracking.

**Table Name**: `tasks`

**Attributes**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier (auto-generated via uuid4()) |
| `user_id` | UUID | FOREIGN KEY → users.id, NOT NULL, INDEXED | Owner of the task |
| `title` | VARCHAR(200) | NOT NULL, INDEXED | Task title (max 200 characters) |
| `description` | VARCHAR(1000) | NULLABLE | Optional task description (max 1000 characters) |
| `completed` | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT UTC NOW | Timestamp when task was created |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT UTC NOW | Timestamp when task was last modified |

**Indexes**:
- PRIMARY KEY on `id`
- INDEX on `user_id` (for efficient user-specific queries)
- INDEX on `title` (for potential search features)

**Relationships**:
- Many-to-One with User (`user_id` → `users.id`)

**Validation Rules**:
- `title` must be 1-200 characters
- `description` must be 0-1000 characters if provided
- `user_id` must reference an existing user

**SQLModel Definition** (`backend/app/models/task.py`):
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200, index=True)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

### 2. Conversation

**Purpose**: Represents a chat session between a user and the AI assistant, containing multiple messages and tracking session metadata.

**Table Name**: `conversations`

**Attributes**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier (auto-generated via uuid4()) |
| `user_id` | UUID | FOREIGN KEY → users.id, NOT NULL, INDEXED | Owner of the conversation |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT UTC NOW | Timestamp when conversation was created |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT UTC NOW | Timestamp of last activity in conversation |

**Indexes**:
- PRIMARY KEY on `id`
- INDEX on `user_id` (for efficient user-specific queries)

**Relationships**:
- Many-to-One with User (`user_id` → `users.id`)
- One-to-Many with Message (cascade delete: deleting conversation deletes all messages)

**Validation Rules**:
- `user_id` must reference an existing user
- Cannot create conversation without user

**Cascade Behavior**:
- **ON DELETE CASCADE**: When a conversation is deleted, all associated messages are automatically removed

**SQLModel Definition** (`backend/app/models/conversation.py`):
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.message import Message

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
```

---

### 3. Message

**Purpose**: Represents a single message within a conversation, storing the content, sender role (user or AI assistant), and linking to the parent conversation.

**Table Name**: `messages`

**Attributes**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier (auto-generated via uuid4()) |
| `conversation_id` | UUID | FOREIGN KEY → conversations.id ON DELETE CASCADE, NOT NULL, INDEXED | Parent conversation |
| `role` | ENUM('user', 'assistant') | NOT NULL | Sender of the message |
| `content` | TEXT | NOT NULL (max 5000 chars in model) | Message text content |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT UTC NOW | Timestamp when message was sent |

**Note**: No `updated_at` field because messages are immutable once created (audit trail integrity).

**Indexes**:
- PRIMARY KEY on `id`
- INDEX on `conversation_id` (for efficient conversation history queries)

**Relationships**:
- Many-to-One with Conversation (`conversation_id` → `conversations.id`)
- **CASCADE DELETE**: Deleted when parent conversation is deleted

**Validation Rules**:
- `role` must be one of: 'user', 'assistant'
- `content` must be 1-5000 characters
- `conversation_id` must reference an existing conversation

**Enum Definition**:
```python
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
```

**SQLModel Definition** (`backend/app/models/message.py`):
```python
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum as SQLAEnum
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.conversation import Conversation

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    role: MessageRole = Field(sa_column=Column(SQLAEnum(MessageRole)))
    content: str = Field(max_length=5000)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
```

---

## Relationship Details

### User → Task (One-to-Many)

- **Cardinality**: One user can have zero or more tasks
- **Ownership**: Tasks are owned by a single user
- **Deletion**: When user is deleted, tasks should be cascade deleted (if user deletion is implemented)
- **Access Control**: Users can only access their own tasks (enforced in API layer via JWT user_id)

### User → Conversation (One-to-Many)

- **Cardinality**: One user can have zero or more conversations
- **Ownership**: Conversations are owned by a single user
- **Deletion**: When user is deleted, conversations should be cascade deleted (if user deletion is implemented)
- **Access Control**: Users can only access their own conversations (enforced in API layer)

### Conversation → Message (One-to-Many with Cascade Delete)

- **Cardinality**: One conversation contains zero or more messages
- **Ownership**: Messages belong to a single conversation
- **Deletion**: **CASCADE DELETE** - When a conversation is deleted, all its messages are automatically removed
- **Immutability**: Messages cannot be edited or deleted individually (only via conversation deletion)
- **Ordering**: Messages are typically ordered by `created_at` ASC to show conversation history chronologically

---

## Database Constraints

### Primary Keys
- All tables use UUID primary keys (not auto-incrementing integers)
- UUIDs are generated using Python's `uuid.uuid4()` function
- Benefits: No sequential ID enumeration attacks, globally unique across distributed systems

### Foreign Keys
```sql
-- Task references User
ALTER TABLE tasks
  ADD CONSTRAINT fk_task_user
  FOREIGN KEY (user_id) REFERENCES users(id);

-- Conversation references User
ALTER TABLE conversations
  ADD CONSTRAINT fk_conversation_user
  FOREIGN KEY (user_id) REFERENCES users(id);

-- Message references Conversation with CASCADE DELETE
ALTER TABLE messages
  ADD CONSTRAINT fk_message_conversation
  FOREIGN KEY (conversation_id) REFERENCES conversations(id)
  ON DELETE CASCADE;
```

### Unique Constraints
- `users.email` is UNIQUE (enforced at database level, not part of this spec)

### Check Constraints (Future Enhancement)
```sql
-- Ensure title is not empty string
ALTER TABLE tasks
  ADD CONSTRAINT check_task_title_not_empty
  CHECK (length(title) > 0);

-- Ensure content is not empty string
ALTER TABLE messages
  ADD CONSTRAINT check_message_content_not_empty
  CHECK (length(content) > 0);
```

---

## Index Strategy

### Performance Optimization

**user_id Indexes** (Multi-Tenant Isolation):
```sql
CREATE INDEX ix_tasks_user_id ON tasks(user_id);
CREATE INDEX ix_conversations_user_id ON conversations(user_id);
```

- **Purpose**: Enable fast filtering of data by user (primary access pattern)
- **Query Pattern**: `WHERE user_id = ?` (used in every user-scoped query)
- **Performance**: Converts O(n) table scan to O(log n) index scan

**conversation_id Index** (Message History):
```sql
CREATE INDEX ix_messages_conversation_id ON messages(conversation_id);
```

- **Purpose**: Fast retrieval of all messages in a conversation
- **Query Pattern**: `WHERE conversation_id = ? ORDER BY created_at ASC`
- **Performance**: Enables efficient pagination of conversation history

**title Index** (Task Search - Future):
```sql
CREATE INDEX ix_tasks_title ON tasks(title);
```

- **Purpose**: Support future full-text search on task titles
- **Query Pattern**: `WHERE title ILIKE ?` or full-text search
- **Status**: Created proactively but not yet utilized in queries

---

## Data Access Patterns

### Common Queries

**1. List User's Tasks**:
```sql
SELECT * FROM tasks
WHERE user_id = $1
ORDER BY created_at DESC;
```
- Uses: `ix_tasks_user_id` index
- Performance: O(log n + m) where m = user's task count

**2. Get Conversation History**:
```sql
SELECT c.*, COUNT(m.id) AS message_count
FROM conversations c
LEFT JOIN messages m ON m.conversation_id = c.id
WHERE c.user_id = $1
GROUP BY c.id
ORDER BY c.updated_at DESC;
```
- Uses: `ix_conversations_user_id` index
- Performance: Efficient with proper index usage

**3. Retrieve Conversation Messages**:
```sql
SELECT * FROM messages
WHERE conversation_id = $1
ORDER BY created_at ASC;
```
- Uses: `ix_messages_conversation_id` index
- Performance: O(log n + m) where m = message count in conversation

**4. Create Task**:
```sql
INSERT INTO tasks (id, user_id, title, description, completed, created_at, updated_at)
VALUES ($1, $2, $3, $4, FALSE, NOW(), NOW());
```
- Performance: O(log n) for index updates

---

## Migration Strategy

### Alembic Migration Files

**Initial Schema Migration**:
- Creates `users`, `tasks` tables
- Establishes foreign keys and indexes
- File: `backend/alembic/versions/xxxxx_initial_schema.py`

**Conversation/Message Migration**:
- Adds `conversations`, `messages` tables
- Configures cascade delete relationship
- File: `backend/alembic/versions/xxxxx_add_conversations_messages.py`

### Migration Commands

```bash
# Apply all pending migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# Show current migration version
alembic current

# View migration history
alembic history

# Generate new migration (after model changes)
alembic revision --autogenerate -m "Descriptive message"
```

---

## Data Lifecycle

### Timestamp Management

**created_at**:
- Automatically set when record is created
- Never modified after creation
- Used for auditing and chronological ordering

**updated_at** (Task, Conversation only):
- Automatically set when record is created
- **Manually updated** in application code when record is modified
- Reflects last modification time

**Example Update Pattern**:
```python
from datetime import datetime

@router.put("/{task_id}")
async def update_task(task_id: UUID, task_update: TaskUpdate, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    task.updated_at = datetime.utcnow()  # Manual timestamp update
    session.add(task)
    session.commit()
    return task
```

### Cascade Deletion

**Conversation Deletion**:
```python
# Deleting conversation automatically deletes all messages
conversation = session.get(Conversation, conversation_id)
session.delete(conversation)
session.commit()  # All messages with conversation_id are removed
```

**Verification**:
```python
# Verify cascade deletion
messages_count = session.exec(
    select(func.count()).select_from(Message).where(Message.conversation_id == deleted_conversation_id)
).one()
assert messages_count == 0  # Should be zero after cascade delete
```

---

## Security Considerations

### User Isolation

**Principle**: Users must only access their own data

**Enforcement Points**:
1. **API Layer**: JWT token extraction and user_id validation
2. **Query Layer**: All queries filtered by `user_id` from token
3. **Database Layer**: Foreign key constraints prevent invalid references

**Example Secure Query**:
```python
# BAD: Trusts user_id from URL parameter
tasks = session.exec(select(Task).where(Task.user_id == user_id_from_url)).all()

# GOOD: Verifies user_id from JWT matches URL parameter
if current_user.id != user_id_from_url:
    raise HTTPException(status_code=403, detail="Not authorized")
tasks = session.exec(select(Task).where(Task.user_id == current_user.id)).all()
```

### SQL Injection Prevention

- **Parameterized Queries**: SQLModel/SQLAlchemy automatically uses parameterized queries
- **No Raw SQL**: Avoid using `session.execute(text(...))` with user input
- **ORM Protection**: All model operations are safe by default

---

## Testing Strategy

### Unit Tests (Isolated Models)

```python
def test_task_creation():
    task = Task(
        user_id=uuid4(),
        title="Test Task",
        description="Test Description"
    )
    assert task.completed is False
    assert task.created_at is not None
```

### Integration Tests (Database Operations)

```python
def test_cascade_delete(session):
    # Create conversation with messages
    conversation = Conversation(user_id=user.id)
    session.add(conversation)
    session.commit()

    message = Message(conversation_id=conversation.id, role=MessageRole.USER, content="Test")
    session.add(message)
    session.commit()

    # Delete conversation
    session.delete(conversation)
    session.commit()

    # Verify messages are deleted
    messages = session.exec(select(Message).where(Message.conversation_id == conversation.id)).all()
    assert len(messages) == 0
```

---

## Conclusion

This data model provides a solid foundation for the Todo Full-Stack Web Application with:
- Clear entity separation (Task for todos, Conversation/Message for AI chat)
- Proper relationships with cascade deletion
- Performance-optimized indexes for multi-tenant queries
- Type-safe SQLModel definitions aligned with PostgreSQL schema
- Comprehensive constraints and validation rules

All entities align with the feature specification (FR-001 through FR-015) and constitution database standards.
