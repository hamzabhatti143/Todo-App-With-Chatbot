# Data Model: Todo AI Chatbot

**Feature**: 013-todo-ai-chatbot
**Date**: 2026-01-16
**Status**: Draft

## Overview

This document defines the database schema for the Todo AI Chatbot feature, extending the existing todo application with conversation history and message storage. The model preserves existing User and Task entities while adding new Conversation and Message entities for chat functionality.

## Entity Relationship Diagram

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │
       │ 1:N
       │
    ┌──┴───────────────┬──────────────────┐
    │                  │                  │
    ▼                  ▼                  ▼
┌─────────┐    ┌─────────────┐   ┌────────────┐
│  Task   │    │Conversation │   │  (other)   │
└─────────┘    └──────┬──────┘   └────────────┘
                      │
                      │ 1:N
                      │
                      ▼
               ┌──────────────┐
               │   Message    │
               └──────────────┘
```

## Entities

### 1. User (Existing - No Changes)

**Purpose**: Represents an authenticated user account.

**SQLModel Definition**:
```python
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships (defined via back_populates in related models)
    tasks: List["Task"] = Relationship(back_populates="user")
    conversations: List["Conversation"] = Relationship(back_populates="user")
```

**Indexes**:
- Primary key on `id` (UUID)
- Unique index on `email`

**Constraints**:
- `email` must be unique
- `email` must be valid email format (validated in Pydantic schema)
- `hashed_password` must be bcrypt hash (validated in auth service)

### 2. Task (Existing - No Changes)

**Purpose**: Represents a todo item created by a user.

**SQLModel Definition**:
```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="tasks")
```

**Indexes**:
- Primary key on `id` (UUID)
- Foreign key index on `user_id`
- Index on `title` (for search, future enhancement)

**Constraints**:
- `user_id` must reference valid user (ON DELETE CASCADE)
- `title` required, max 200 characters
- `description` optional, max 1000 characters
- `completed` defaults to False

### 3. Conversation (New)

**Purpose**: Represents a chat conversation between a user and the AI agent. Groups related messages together.

**SQLModel Definition**:
```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
```

**Indexes**:
- Primary key on `id` (UUID)
- Foreign key index on `user_id` (for listing user conversations)
- Index on `created_at` (for sorting conversations by recency)

**Constraints**:
- `user_id` must reference valid user (ON DELETE CASCADE)
- `created_at` auto-generated on insert
- `updated_at` auto-updated on message addition

**State Transitions**:
- `created` - Conversation created when first message sent
- `active` - Conversation has ongoing messages (implicit state, no status field)

### 4. Message (New)

**Purpose**: Represents a single message in a conversation, either from the user or the AI assistant.

**SQLModel Definition**:
```python
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    role: MessageRole = Field(sa_column=Column(Enum(MessageRole)))
    content: str = Field(max_length=5000)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
```

**Indexes**:
- Primary key on `id` (UUID)
- Foreign key index on `conversation_id` (for retrieving conversation history)
- Index on `created_at` (for ordering messages chronologically)

**Constraints**:
- `conversation_id` must reference valid conversation (ON DELETE CASCADE)
- `role` must be either "user" or "assistant" (enum constraint)
- `content` required, min 1 character, max 5000 characters
- `created_at` auto-generated on insert
- Messages are immutable (no updates or deletes in MVP)

**Validation Rules** (Pydantic Schema):
```python
class MessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)

    @validator('content')
    def content_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Message content cannot be empty or whitespace')
        return v
```

### 5. MCP Tool (Logical Entity - Not a Database Table)

**Purpose**: Represents the MCP tools exposed to the Gemini AI agent for task operations. These are code-based tool definitions, not database records.

**Tool Definitions**:

#### add_task
```python
@mcp_tool
def add_task(title: str, description: str | None, user_id: UUID) -> Task:
    """
    Create a new task for the user.

    Args:
        title: Task title (1-200 characters)
        description: Optional task description (max 1000 characters)
        user_id: User ID from conversation context

    Returns:
        Created Task object with id, title, description, completed, timestamps
    """
    pass
```

#### list_tasks
```python
@mcp_tool
def list_tasks(user_id: UUID, completed: bool | None = None) -> List[Task]:
    """
    List all tasks for the user, optionally filtered by completion status.

    Args:
        user_id: User ID from conversation context
        completed: Optional filter (True=completed, False=incomplete, None=all)

    Returns:
        List of Task objects ordered by created_at descending
    """
    pass
```

#### complete_task
```python
@mcp_tool
def complete_task(task_id: UUID, user_id: UUID) -> Task:
    """
    Mark a task as completed (toggle completion status).

    Args:
        task_id: Task ID to complete
        user_id: User ID from conversation context (for ownership verification)

    Returns:
        Updated Task object with completed=True

    Raises:
        NotFoundError: Task not found or not owned by user
    """
    pass
```

#### update_task
```python
@mcp_tool
def update_task(
    task_id: UUID,
    user_id: UUID,
    title: str | None = None,
    description: str | None = None
) -> Task:
    """
    Update task title and/or description.

    Args:
        task_id: Task ID to update
        user_id: User ID from conversation context (for ownership verification)
        title: Optional new title (1-200 characters)
        description: Optional new description (max 1000 characters)

    Returns:
        Updated Task object with modified fields and updated_at timestamp

    Raises:
        NotFoundError: Task not found or not owned by user
        ValueError: Invalid title or description
    """
    pass
```

#### delete_task
```python
@mcp_tool
def delete_task(task_id: UUID, user_id: UUID) -> bool:
    """
    Delete a task permanently.

    Args:
        task_id: Task ID to delete
        user_id: User ID from conversation context (for ownership verification)

    Returns:
        True if task was deleted successfully

    Raises:
        NotFoundError: Task not found or not owned by user
    """
    pass
```

**MCP Tool Registration**:
- Tools registered with Gemini agent at FastAPI startup
- Each tool has input schema (Pydantic model) and output schema
- Tool execution results sent back to AI agent for response generation

## Database Migrations

### Migration: Add Conversations and Messages Tables

**File**: `backend/alembic/versions/003_add_conversations_messages.py`

**Operations**:

1. **Create `conversations` table**:
   ```sql
   CREATE TABLE conversations (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
       created_at TIMESTAMP NOT NULL DEFAULT NOW(),
       updated_at TIMESTAMP NOT NULL DEFAULT NOW()
   );

   CREATE INDEX ix_conversations_user_id ON conversations(user_id);
   CREATE INDEX ix_conversations_created_at ON conversations(created_at);
   ```

2. **Create `messages` table**:
   ```sql
   CREATE TYPE message_role AS ENUM ('user', 'assistant');

   CREATE TABLE messages (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
       role message_role NOT NULL,
       content TEXT NOT NULL CHECK (length(content) <= 5000),
       created_at TIMESTAMP NOT NULL DEFAULT NOW()
   );

   CREATE INDEX ix_messages_conversation_id ON messages(conversation_id);
   CREATE INDEX ix_messages_created_at ON messages(created_at);
   ```

3. **Update User model** (if needed):
   - No schema changes required
   - Relationships defined in SQLModel code only

**Rollback**:
```sql
DROP TABLE messages;
DROP TABLE conversations;
DROP TYPE message_role;
```

## Validation Rules

### Message Validation

**Content Validation**:
- Minimum length: 1 character (after trimming whitespace)
- Maximum length: 5000 characters
- Cannot be empty string or whitespace only

**Role Validation**:
- Must be either "user" or "assistant" (enum constraint)
- Frontend sends "user" messages only
- Backend creates "assistant" messages from AI responses

### Task Validation (Existing Rules)

**Title Validation**:
- Required field
- Minimum length: 1 character
- Maximum length: 200 characters

**Description Validation**:
- Optional field (can be null)
- Maximum length: 1000 characters

### Conversation Validation

**User Ownership**:
- All conversation queries must filter by JWT user_id
- Prevents cross-user conversation access
- Enforced at API layer (not database constraint)

## Query Patterns

### User Conversations Query

**Use Case**: List all conversations for a user (for conversation history sidebar)

```python
def get_user_conversations(user_id: UUID, limit: int = 50) -> List[Conversation]:
    """
    Retrieve user's conversations ordered by most recent first.

    SELECT * FROM conversations
    WHERE user_id = :user_id
    ORDER BY updated_at DESC
    LIMIT :limit
    """
    return session.exec(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
    ).all()
```

**Performance**: Index on `user_id` enables efficient filtering. Index on `updated_at` enables efficient sorting.

### Conversation Messages Query

**Use Case**: Retrieve all messages in a conversation (for chat history display)

```python
def get_conversation_messages(
    conversation_id: UUID,
    user_id: UUID
) -> List[Message]:
    """
    Retrieve all messages in a conversation, ordered chronologically.
    Verifies conversation belongs to user.

    SELECT m.* FROM messages m
    JOIN conversations c ON m.conversation_id = c.id
    WHERE m.conversation_id = :conversation_id
    AND c.user_id = :user_id
    ORDER BY m.created_at ASC
    """
    # Verify ownership first
    conversation = session.get(Conversation, conversation_id)
    if not conversation or conversation.user_id != user_id:
        raise NotFoundError("Conversation not found")

    return session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    ).all()
```

**Performance**: Index on `conversation_id` enables efficient message retrieval. Index on `created_at` enables chronological ordering.

### Task Queries (Existing - Used by MCP Tools)

**List User Tasks**:
```python
def list_user_tasks(user_id: UUID, completed: bool | None = None) -> List[Task]:
    """
    SELECT * FROM tasks
    WHERE user_id = :user_id
    [AND completed = :completed]
    ORDER BY created_at DESC
    """
    query = select(Task).where(Task.user_id == user_id)
    if completed is not None:
        query = query.where(Task.completed == completed)
    return session.exec(query.order_by(Task.created_at.desc())).all()
```

**Get Task by ID with Ownership Check**:
```python
def get_task_for_user(task_id: UUID, user_id: UUID) -> Task:
    """
    SELECT * FROM tasks
    WHERE id = :task_id AND user_id = :user_id
    """
    task = session.exec(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.user_id == user_id)
    ).first()
    if not task:
        raise NotFoundError("Task not found")
    return task
```

## Security Considerations

### User Isolation

**Principle**: Every database query MUST filter by user_id from JWT token.

**Enforcement**:
1. **API Layer**: Extract user_id from JWT token in auth middleware
2. **Service Layer**: Pass user_id to all service methods as required parameter
3. **MCP Tool Layer**: Tools receive user_id from conversation context
4. **Database Layer**: All queries include `WHERE user_id = :user_id` filter

**Example - Preventing Cross-User Access**:
```python
# BAD: No user_id filter
conversation = session.get(Conversation, conversation_id)  # Vulnerable!

# GOOD: Verify ownership
conversation = session.exec(
    select(Conversation)
    .where(Conversation.id == conversation_id)
    .where(Conversation.user_id == user_id)
).first()
```

### Cascade Deletes

**User Deletion**: Deleting a user cascades to:
- All user's tasks (ON DELETE CASCADE)
- All user's conversations (ON DELETE CASCADE)
  - Which cascades to all messages in those conversations (ON DELETE CASCADE)

**Conversation Deletion**: Deleting a conversation cascades to:
- All messages in that conversation (ON DELETE CASCADE)

**Rationale**: Prevents orphaned records. User data must be fully removed on account deletion.

## Performance Optimization

### Index Strategy

**Critical Indexes** (already included):
1. `conversations.user_id` - For listing user conversations
2. `conversations.created_at` - For sorting by recency
3. `messages.conversation_id` - For retrieving conversation messages
4. `messages.created_at` - For chronological ordering
5. `tasks.user_id` - For listing user tasks (existing)

**Future Indexes** (if needed):
- Full-text search on `messages.content` (for message search)
- Full-text search on `tasks.title` (for task search)

### Query Optimization

**N+1 Query Prevention**:
- Use `selectinload()` or `joinedload()` for eager loading relationships
- Example: Loading conversations with message count

```python
from sqlalchemy.orm import selectinload

conversations = session.exec(
    select(Conversation)
    .where(Conversation.user_id == user_id)
    .options(selectinload(Conversation.messages))
    .order_by(Conversation.updated_at.desc())
).all()
```

### Pagination

**Conversation Listing**:
- Default limit: 50 conversations
- Use cursor-based pagination for large conversation lists

**Message Retrieval**:
- Load all messages for a conversation (no pagination in MVP)
- Future: Paginate if conversation exceeds 100 messages

## Testing Considerations

### Unit Tests

**Model Validation Tests**:
```python
def test_message_content_max_length():
    """Message content cannot exceed 5000 characters"""
    long_content = "a" * 5001
    with pytest.raises(ValidationError):
        Message(conversation_id=uuid4(), role=MessageRole.USER, content=long_content)

def test_message_role_enum():
    """Message role must be 'user' or 'assistant'"""
    with pytest.raises(ValidationError):
        Message(conversation_id=uuid4(), role="invalid", content="test")
```

### Integration Tests

**Conversation Ownership Tests**:
```python
def test_user_cannot_access_other_user_conversation():
    """User A cannot retrieve User B's conversation"""
    user_a = create_user("a@example.com")
    user_b = create_user("b@example.com")
    conv_b = create_conversation(user_b.id)

    # Attempt to access User B's conversation as User A
    response = client.get(
        f"/api/conversations/{conv_b.id}",
        headers={"Authorization": f"Bearer {get_token(user_a.id)}"}
    )
    assert response.status_code == 404  # Not found (not 403, to avoid leaking existence)
```

**MCP Tool Ownership Tests**:
```python
def test_mcp_complete_task_requires_ownership():
    """complete_task tool cannot complete another user's task"""
    user_a = create_user("a@example.com")
    user_b = create_user("b@example.com")
    task_b = create_task(user_b.id, "Task B")

    # Attempt to complete User B's task via MCP tool with User A's context
    with pytest.raises(NotFoundError):
        complete_task(task_id=task_b.id, user_id=user_a.id)
```

## Summary

This data model extends the existing todo application with conversation and message storage while maintaining:
- ✅ Complete user data isolation via user_id filtering
- ✅ Referential integrity via foreign key constraints
- ✅ Efficient queries via strategic indexes
- ✅ Data consistency via cascade deletes
- ✅ Type safety via SQLModel and Pydantic
- ✅ Scalability via stateless design (no in-memory sessions)

All new entities integrate seamlessly with the existing User and Task models, requiring only a single Alembic migration to implement.
