-- Database Schema for Todo Full-Stack Web Application
-- Feature: 014-database-models
-- Generated: 2026-01-16
-- Database: PostgreSQL 16 (Neon Serverless)

-- ============================================================================
-- EXTENSIONS
-- ============================================================================

-- Enable UUID generation (if not already enabled)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- ENUMERATIONS
-- ============================================================================

-- Message role enumeration
CREATE TYPE message_role AS ENUM ('user', 'assistant');

-- ============================================================================
-- TABLES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Users Table (existing, referenced by other tables)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),
    updated_at TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc')
);

-- Index for email lookups
CREATE INDEX IF NOT EXISTS ix_users_email ON users(email);

-- ----------------------------------------------------------------------------
-- Tasks Table
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),
    updated_at TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),

    -- Foreign key constraint
    CONSTRAINT fk_task_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    -- Validation constraints
    CONSTRAINT check_task_title_not_empty
        CHECK (length(trim(title)) > 0),

    CONSTRAINT check_task_title_length
        CHECK (length(title) <= 200),

    CONSTRAINT check_task_description_length
        CHECK (description IS NULL OR length(description) <= 1000)
);

-- Indexes for query optimization
CREATE INDEX IF NOT EXISTS ix_tasks_user_id ON tasks(user_id);
CREATE INDEX IF NOT EXISTS ix_tasks_title ON tasks(title);
CREATE INDEX IF NOT EXISTS ix_tasks_created_at ON tasks(created_at);

-- Composite index for common query pattern: user's incomplete tasks
CREATE INDEX IF NOT EXISTS ix_tasks_user_completed ON tasks(user_id, completed);

COMMENT ON TABLE tasks IS 'User todo tasks with title, description, and completion status';
COMMENT ON COLUMN tasks.id IS 'Unique task identifier';
COMMENT ON COLUMN tasks.user_id IS 'Owner of the task (foreign key to users.id)';
COMMENT ON COLUMN tasks.title IS 'Task title (1-200 characters)';
COMMENT ON COLUMN tasks.description IS 'Optional task description (max 1000 characters)';
COMMENT ON COLUMN tasks.completed IS 'Task completion status (default: false)';
COMMENT ON COLUMN tasks.created_at IS 'Timestamp when task was created (UTC)';
COMMENT ON COLUMN tasks.updated_at IS 'Timestamp when task was last modified (UTC)';

-- ----------------------------------------------------------------------------
-- Conversations Table
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),
    updated_at TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),

    -- Foreign key constraint
    CONSTRAINT fk_conversation_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- Indexes for query optimization
CREATE INDEX IF NOT EXISTS ix_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS ix_conversations_updated_at ON conversations(updated_at DESC);

-- Composite index for user's recent conversations
CREATE INDEX IF NOT EXISTS ix_conversations_user_updated ON conversations(user_id, updated_at DESC);

COMMENT ON TABLE conversations IS 'Chat sessions between users and AI assistant';
COMMENT ON COLUMN conversations.id IS 'Unique conversation identifier';
COMMENT ON COLUMN conversations.user_id IS 'Owner of the conversation (foreign key to users.id)';
COMMENT ON COLUMN conversations.created_at IS 'Timestamp when conversation was started (UTC)';
COMMENT ON COLUMN conversations.updated_at IS 'Timestamp of last activity in conversation (UTC)';

-- ----------------------------------------------------------------------------
-- Messages Table
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL,
    role message_role NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),

    -- Foreign key constraint with CASCADE DELETE
    CONSTRAINT fk_message_conversation
        FOREIGN KEY (conversation_id)
        REFERENCES conversations(id)
        ON DELETE CASCADE,

    -- Validation constraints
    CONSTRAINT check_message_content_not_empty
        CHECK (length(trim(content)) > 0),

    CONSTRAINT check_message_content_length
        CHECK (length(content) <= 5000)
);

-- Indexes for query optimization
CREATE INDEX IF NOT EXISTS ix_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS ix_messages_created_at ON messages(created_at);

-- Composite index for conversation message history
CREATE INDEX IF NOT EXISTS ix_messages_conversation_created ON messages(conversation_id, created_at ASC);

COMMENT ON TABLE messages IS 'Individual messages within chat conversations';
COMMENT ON COLUMN messages.id IS 'Unique message identifier';
COMMENT ON COLUMN messages.conversation_id IS 'Parent conversation (foreign key to conversations.id, CASCADE DELETE)';
COMMENT ON COLUMN messages.role IS 'Sender role: "user" (human) or "assistant" (AI)';
COMMENT ON COLUMN messages.content IS 'Message text content (1-5000 characters)';
COMMENT ON COLUMN messages.created_at IS 'Timestamp when message was sent (UTC)';

-- ============================================================================
-- FUNCTIONS & TRIGGERS
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Function to auto-update updated_at timestamp
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = (NOW() AT TIME ZONE 'utc');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to tasks table
DROP TRIGGER IF EXISTS update_tasks_updated_at ON tasks;
CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Apply trigger to conversations table
DROP TRIGGER IF EXISTS update_conversations_updated_at ON conversations;
CREATE TRIGGER update_conversations_updated_at
    BEFORE UPDATE ON conversations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Apply trigger to users table
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

COMMENT ON FUNCTION update_updated_at_column() IS 'Automatically updates updated_at timestamp on row modification';

-- ============================================================================
-- VIEWS (Optional - for convenience)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- View: Conversation Summary
-- Provides conversation metadata with message counts
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW conversation_summary AS
SELECT
    c.id AS conversation_id,
    c.user_id,
    c.created_at,
    c.updated_at,
    COUNT(m.id) AS message_count,
    MAX(m.created_at) AS last_message_at
FROM conversations c
LEFT JOIN messages m ON m.conversation_id = c.id
GROUP BY c.id, c.user_id, c.created_at, c.updated_at;

COMMENT ON VIEW conversation_summary IS 'Conversation metadata with message counts and last message timestamp';

-- ----------------------------------------------------------------------------
-- View: User Task Statistics
-- Provides task completion statistics per user
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW user_task_stats AS
SELECT
    user_id,
    COUNT(*) AS total_tasks,
    SUM(CASE WHEN completed THEN 1 ELSE 0 END) AS completed_tasks,
    SUM(CASE WHEN NOT completed THEN 1 ELSE 0 END) AS pending_tasks,
    ROUND(
        100.0 * SUM(CASE WHEN completed THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0),
        2
    ) AS completion_percentage
FROM tasks
GROUP BY user_id;

COMMENT ON VIEW user_task_stats IS 'Task completion statistics aggregated by user';

-- ============================================================================
-- SAMPLE QUERIES
-- ============================================================================

-- Query 1: Get user's incomplete tasks ordered by creation date
-- SELECT * FROM tasks
-- WHERE user_id = 'user-uuid-here' AND completed = FALSE
-- ORDER BY created_at DESC;

-- Query 2: Get conversation history with message counts
-- SELECT * FROM conversation_summary
-- WHERE user_id = 'user-uuid-here'
-- ORDER BY updated_at DESC;

-- Query 3: Retrieve messages for a specific conversation
-- SELECT * FROM messages
-- WHERE conversation_id = 'conversation-uuid-here'
-- ORDER BY created_at ASC;

-- Query 4: Get user's task completion statistics
-- SELECT * FROM user_task_stats
-- WHERE user_id = 'user-uuid-here';

-- Query 5: Search tasks by title (case-insensitive)
-- SELECT * FROM tasks
-- WHERE user_id = 'user-uuid-here' AND title ILIKE '%search-term%'
-- ORDER BY created_at DESC;

-- ============================================================================
-- PERFORMANCE VERIFICATION
-- ============================================================================

-- Verify indexes are being used (run EXPLAIN ANALYZE):
-- EXPLAIN ANALYZE SELECT * FROM tasks WHERE user_id = 'uuid-here';
-- Should show: Index Scan using ix_tasks_user_id

-- EXPLAIN ANALYZE SELECT * FROM messages WHERE conversation_id = 'uuid-here';
-- Should show: Index Scan using ix_messages_conversation_id

-- ============================================================================
-- DATA INTEGRITY TESTS
-- ============================================================================

-- Test 1: Verify cascade deletion
-- BEGIN;
-- INSERT INTO conversations (id, user_id) VALUES ('test-conv-uuid', 'user-uuid');
-- INSERT INTO messages (id, conversation_id, role, content)
-- VALUES ('test-msg-uuid', 'test-conv-uuid', 'user', 'Test message');
-- DELETE FROM conversations WHERE id = 'test-conv-uuid';
-- SELECT COUNT(*) FROM messages WHERE id = 'test-msg-uuid'; -- Should return 0
-- ROLLBACK;

-- Test 2: Verify foreign key constraint
-- BEGIN;
-- INSERT INTO tasks (user_id, title) VALUES ('non-existent-user-uuid', 'Test');
-- -- Should fail with foreign key violation
-- ROLLBACK;

-- Test 3: Verify check constraints
-- BEGIN;
-- INSERT INTO tasks (user_id, title) VALUES ('valid-user-uuid', ''); -- Should fail
-- INSERT INTO messages (conversation_id, role, content) VALUES ('valid-conv-uuid', 'user', ''); -- Should fail
-- ROLLBACK;

-- ============================================================================
-- MIGRATION NOTES
-- ============================================================================

-- This schema file represents the target state after applying all migrations.
-- For version-controlled schema changes, use Alembic migrations:
--
-- 1. Generate migration after model changes:
--    alembic revision --autogenerate -m "Description"
--
-- 2. Review generated migration file in alembic/versions/
--
-- 3. Apply migration:
--    alembic upgrade head
--
-- 4. Rollback if needed:
--    alembic downgrade -1
--
-- Never apply this schema.sql directly to production - use Alembic migrations.

-- ============================================================================
-- SECURITY NOTES
-- ============================================================================

-- 1. User Isolation: All queries must filter by user_id from JWT token
-- 2. SQL Injection: Use parameterized queries via SQLModel/SQLAlchemy
-- 3. SSL Required: Connection string must include ?sslmode=require
-- 4. Row-Level Security: Consider implementing RLS for additional protection
-- 5. Audit Logging: created_at fields provide basic audit trail

-- Example Row-Level Security Policy (optional, not currently implemented):
-- ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY tasks_isolation_policy ON tasks
--     USING (user_id = current_setting('app.current_user_id')::uuid);

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
