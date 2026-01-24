# Data Model: Stateless Chat API Backend

**Feature**: 017-chat-api
**Date**: 2026-01-18
**Status**: Implemented (Feature 014)

## Overview

This document describes the database schema for the chat API backend. The data models were implemented in Feature 014 (Database Models) and are reused by this feature. No new tables are required.

## Entity Relationship Diagram

```
┌─────────────────────┐
│      users          │
│─────────────────────│
│ id: UUID (PK)       │
│ email: VARCHAR(255) │
│ hashed_password:    │
│   VARCHAR(255)      │
│ created_at: TIMESTAMP│
└─────────────────────┘
          │
          │ 1:N
          ▼
┌─────────────────────┐
│   conversations     │
│─────────────────────│
│ id: UUID (PK)       │
│ user_id: UUID (FK)  │───┐ References users.id
│ created_at: TIMESTAMP│   │ ON DELETE CASCADE
│ updated_at: TIMESTAMP│   │
└─────────────────────┘   │
          │               │
          │ 1:N           │
          ▼               │
┌─────────────────────┐   │
│     messages        │   │
│─────────────────────│   │
│ id: UUID (PK)       │   │
│ conversation_id:    │───┘ References conversations.id
│   UUID (FK)         │     ON DELETE CASCADE
│ role: ENUM          │     ('user', 'assistant')
│ content: TEXT       │     (max 5000 chars)
│ created_at: TIMESTAMP│
└─────────────────────┘
```

## Entities

### 1. Conversation

**Purpose**: Represents a chat conversation between a user and the AI assistant.

**Table Name**: `conversations`

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique conversation identifier |
| `user_id` | UUID | FOREIGN KEY → users.id, NOT NULL, INDEX | Owner of the conversation |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | When conversation was created |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last message timestamp |

**Indexes**:
```sql
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at);
```

**Foreign Keys**:
```sql
ALTER TABLE conversations
  ADD CONSTRAINT fk_conversations_user_id
  FOREIGN KEY (user_id) REFERENCES users(id)
  ON DELETE CASCADE;
```

**SQLModel Definition** (`models/conversation.py`):
```python
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Validation Rules**:
- `user_id` must reference an existing user
- `updated_at` must be >= `created_at`
- Conversation belongs to exactly one user (1:1 relationship)

**Business Rules**:
- When user creates first message without conversation_id, create new conversation
- When user sends message with conversation_id, verify ownership (user_id matches JWT)
- Deleting user cascades to delete all their conversations
- Deleting conversation cascades to delete all its messages

---

### 2. Message

**Purpose**: Represents a single message within a conversation (user or assistant).

**Table Name**: `messages`

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique message identifier |
| `conversation_id` | UUID | FOREIGN KEY → conversations.id, NOT NULL, INDEX | Parent conversation |
| `role` | ENUM('user', 'assistant') | NOT NULL | Message sender role |
| `content` | TEXT | NOT NULL, CHECK(LENGTH(content) <= 5000) | Message text content |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | When message was created |

**Indexes**:
```sql
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at);
```

**Foreign Keys**:
```sql
ALTER TABLE messages
  ADD CONSTRAINT fk_messages_conversation_id
  FOREIGN KEY (conversation_id) REFERENCES conversations(id)
  ON DELETE CASCADE;
```

**SQLModel Definition** (`models/message.py`):
```python
from sqlmodel import SQLModel, Field, Column, Enum as SQLAEnum
from sqlalchemy import Enum as SAEnum
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

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
```

**Validation Rules**:
- `conversation_id` must reference an existing conversation
- `role` must be either "user" or "assistant"
- `content` length: 1-5000 characters
- Messages are immutable (no updates, only create/delete)

**Business Rules**:
- User messages stored BEFORE invoking AI agent (data loss prevention)
- Assistant messages stored AFTER agent completes successfully
- Conversation history limited to last 20 messages when passed to agent
- Messages ordered chronologically by `created_at` (ascending)

---

## Relationships

### User → Conversations (1:N)
- One user has many conversations
- Deleting user cascades to conversations
- User isolation enforced: user can only access their own conversations

### Conversation → Messages (1:N)
- One conversation has many messages
- Deleting conversation cascades to messages
- Messages alternate between user and assistant roles
- Minimum 1 message per conversation (user's first message)

---

## Queries

### 1. Create New Conversation

**Used In**: POST /api/chat (when conversation_id is null)

```python
conversation = Conversation(user_id=current_user.id)
session.add(conversation)
session.commit()
session.refresh(conversation)
```

**SQL Equivalent**:
```sql
INSERT INTO conversations (id, user_id, created_at, updated_at)
VALUES (uuid_generate_v4(), $1, NOW(), NOW())
RETURNING id, user_id, created_at, updated_at;
```

---

### 2. Get Conversation (with Ownership Validation)

**Used In**: POST /api/chat (when conversation_id provided)

```python
statement = select(Conversation).where(
    Conversation.id == conversation_id,
    Conversation.user_id == current_user.id
)
conversation = session.exec(statement).first()
```

**SQL Equivalent**:
```sql
SELECT id, user_id, created_at, updated_at
FROM conversations
WHERE id = $1 AND user_id = $2
LIMIT 1;
```

**Performance**: Uses index on `id` (PK) and `user_id` (indexed)

---

### 3. Save Message

**Used In**: POST /api/chat (save user message, save assistant message)

```python
message = Message(
    conversation_id=conversation.id,
    role=MessageRole.USER,  # or MessageRole.ASSISTANT
    content=request.content
)
session.add(message)
session.commit()
session.refresh(message)
```

**SQL Equivalent**:
```sql
INSERT INTO messages (id, conversation_id, role, content, created_at)
VALUES (uuid_generate_v4(), $1, $2, $3, NOW())
RETURNING id, conversation_id, role, content, created_at;
```

---

### 4. Get Conversation History (Last 20 Messages)

**Used In**: POST /api/chat (retrieve context for agent)

```python
statement = (
    select(Message)
    .where(Message.conversation_id == conversation_id)
    .order_by(Message.created_at.desc())
    .limit(20)
)
messages = session.exec(statement).all()
messages.reverse()  # Chronological order for agent
```

**SQL Equivalent**:
```sql
SELECT id, conversation_id, role, content, created_at
FROM messages
WHERE conversation_id = $1
ORDER BY created_at DESC
LIMIT 20;
```

**Performance**: Uses composite index `idx_messages_conversation_created` (conversation_id, created_at)

**Result Processing**: Reverse list to get chronological order (oldest first)

---

## State Transitions

### Conversation Lifecycle

```
┌─────────────┐
│   Created   │ User sends first message (POST /api/chat with conversation_id=null)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Active    │ User and assistant exchange messages
│             │ (POST /api/chat with existing conversation_id)
└──────┬──────┘
       │
       │ (No explicit end state - conversation remains indefinitely)
       │
       ▼
┌─────────────┐
│  Archived   │ (Future: soft delete or archive feature)
└─────────────┘
```

### Message Lifecycle

```
┌──────────────┐
│  User Input  │ User types message in frontend
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Saved to DB  │ Message persisted BEFORE agent invocation
│  (role=user) │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Agent        │ TodoBot processes message
│ Processing   │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ Assistant Response│ Agent response saved to DB
│ Saved to DB      │ (role=assistant)
│                  │
└──────────────────┘
       │
       ▼
┌──────────────┐
│  Immutable   │ Messages never updated or deleted (append-only)
└──────────────┘
```

---

## Data Constraints

### Conversation Constraints

1. **User Ownership**: Every conversation belongs to exactly one user
2. **Timestamps**: `updated_at` >= `created_at`
3. **Non-Empty**: Every conversation must have at least one message
4. **UUID Uniqueness**: `id` is globally unique (UUID v4)

### Message Constraints

1. **Conversation Membership**: Every message belongs to exactly one conversation
2. **Role Validation**: `role` must be 'user' or 'assistant'
3. **Content Length**: 1-5000 characters (enforced by Pydantic and DB check)
4. **Immutability**: Messages are never updated (INSERT and SELECT only)
5. **Timestamp Order**: Within a conversation, messages ordered by `created_at`

---

## Migration History

**Implemented In**: Feature 014 (Database Models)

**Migration Files**:
- `backend/alembic/versions/xxx_add_conversations_table.py`
- `backend/alembic/versions/xxx_add_messages_table.py`

**Status**: ✅ Applied to database

---

## Performance Considerations

### Indexing Strategy

| Index | Purpose | Query Benefit |
|-------|---------|---------------|
| `conversations(id)` | PK lookup | Get conversation by ID |
| `conversations(user_id)` | User isolation | List user's conversations |
| `conversations(created_at)` | Chronological sorting | Recent conversations |
| `messages(id)` | PK lookup | Get message by ID |
| `messages(conversation_id)` | Conversation filtering | Get all messages in conversation |
| `messages(created_at)` | Chronological sorting | Recent messages |
| `messages(conversation_id, created_at)` | Combined filter + sort | **Most important**: Get last 20 messages |

### Query Performance

| Query | Expected Time | Bottleneck |
|-------|--------------|------------|
| Get conversation by ID | <10ms | Indexed PK lookup |
| Get last 20 messages | <50ms | Composite index scan |
| Create conversation | <20ms | Single INSERT |
| Create message | <20ms | Single INSERT |

### Scaling Considerations

1. **Message Count Growth**:
   - Conversations can have unlimited messages
   - Last 20 messages limit prevents unbounded context
   - Future: Consider pagination for conversation history endpoint

2. **Connection Pooling**:
   - SQLModel uses connection pool (configured in database.py)
   - Default pool size: 20 connections
   - Sufficient for 100 concurrent requests (stateless)

3. **Index Maintenance**:
   - Composite index `(conversation_id, created_at)` supports DESC order
   - B-tree index efficient for range scans
   - No full table scans in critical path

---

## Security & Privacy

### User Isolation

**Enforcement Points**:
1. **Database Level**: Foreign key constraint (conversation.user_id → users.id)
2. **Service Level**: ConversationService validates user_id in all queries
3. **Endpoint Level**: JWT token provides authenticated user context

**Query Pattern**:
```python
# CORRECT: Always filter by authenticated user
statement = select(Conversation).where(
    Conversation.id == conversation_id,
    Conversation.user_id == current_user.id  # ← User isolation
)

# INCORRECT: Missing user_id filter (security vulnerability)
statement = select(Conversation).where(
    Conversation.id == conversation_id
)
```

### Data Retention

**Current Policy**: Indefinite retention (messages never deleted)

**Future Considerations**:
- Implement soft delete for conversations
- Add `deleted_at` timestamp column
- Retention policy: 90 days after deletion
- GDPR compliance: User data export and deletion

---

## Example Data

### Conversation Record

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "770e8400-e29b-41d4-a716-446655440002",
  "created_at": "2026-01-16T10:00:00Z",
  "updated_at": "2026-01-16T10:05:00Z"
}
```

### Message Records (in same conversation)

```json
[
  {
    "id": "880e8400-e29b-41d4-a716-446655440003",
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "role": "user",
    "content": "Add buy groceries tomorrow",
    "created_at": "2026-01-16T10:00:00Z"
  },
  {
    "id": "990e8400-e29b-41d4-a716-446655440004",
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "role": "assistant",
    "content": "I've created a task titled 'Buy groceries' for tomorrow. Would you like me to add any specific items to the description?",
    "created_at": "2026-01-16T10:00:05Z"
  },
  {
    "id": "aa0e8400-e29b-41d4-a716-446655440005",
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "role": "user",
    "content": "Yes, add milk, bread, and eggs",
    "created_at": "2026-01-16T10:01:00Z"
  },
  {
    "id": "bb0e8400-e29b-41d4-a716-446655440006",
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "role": "assistant",
    "content": "I've updated the task to include: milk, bread, and eggs",
    "created_at": "2026-01-16T10:01:05Z"
  }
]
```

---

## Status

**Implementation Status**: ✅ Complete (Feature 014)

**Verification**:
- Database tables created via Alembic migrations
- SQLModel models tested with in-memory SQLite (pytest)
- Foreign key constraints enforced
- Indexes created and verified

**Next Steps**: No database changes required for Feature 017 (reuse existing schema)

---

**Last Updated**: 2026-01-18
