# Tasks: Database Models and Migrations

**Input**: Design documents from `/specs/014-database-models/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in specification. Focus is on validation and documentation.

**Organization**: Tasks are grouped by user story to enable independent validation and testing of each story.

**IMPORTANT DISCOVERY**: The database models, Alembic configuration, and connection setup already exist in the codebase (from features 002-database-schema and 013-todo-ai-chatbot). These tasks focus on **validation**, **testing**, and **documentation** rather than new implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app structure**: `backend/app/` for application code, `backend/alembic/` for migrations
- All file paths are absolute from repository root

---

## Phase 1: Setup (Documentation Review)

**Purpose**: Review existing implementation and prepare validation environment

- [ ] T001 Review existing models in backend/app/models/ directory against specification requirements FR-001 through FR-015
- [ ] T002 [P] Review existing database.py configuration in backend/app/database.py for connection pooling and SSL settings
- [ ] T003 [P] Review existing Alembic configuration in backend/alembic.ini and backend/alembic/env.py
- [ ] T004 [P] Verify .env.example includes all required DATABASE_URL and configuration variables
- [ ] T005 Create test environment by copying .env.example to .env.test in backend/ directory

---

## Phase 2: Foundational (Environment Setup)

**Purpose**: Ensure development environment is properly configured for validation testing

**⚠️ CRITICAL**: These tasks must be complete before validation testing can begin

- [ ] T006 Install Python dependencies from backend/requirements.txt (sqlmodel, alembic, psycopg2-binary, pytest)
- [ ] T007 Verify DATABASE_URL in backend/.env points to valid Neon PostgreSQL instance with SSL
- [ ] T008 Test database connection using python script in backend/test_connection.py
- [ ] T009 Check Alembic migration history with `alembic history` command in backend/ directory
- [ ] T010 Verify current migration version with `alembic current` command in backend/ directory

**Checkpoint**: Environment configured and ready for user story validation

---

## Phase 3: User Story 1 - Database Schema Definition (Priority: P1) 🎯 MVP

**Goal**: Validate that all database models are correctly defined with proper types, constraints, relationships, and indexes

**Independent Test**: Apply migrations to a test database and verify table structure matches model definitions using SQL inspection

### Validation for User Story 1

- [ ] T011 [P] [US1] Validate Task model in backend/app/models/task.py matches FR-001 requirements (UUID id, user_id indexed, title max 200, description max 1000, completed bool, timestamps)
- [ ] T012 [P] [US1] Validate Conversation model in backend/app/models/conversation.py matches FR-002 requirements (UUID id, user_id indexed, timestamps, relationship to Message)
- [ ] T013 [P] [US1] Validate Message model in backend/app/models/message.py matches FR-003 requirements (UUID id, conversation_id FK, role enum, content text, created_at, no updated_at by design)
- [ ] T014 [US1] Verify cascade delete relationship in backend/app/models/conversation.py (sa_relationship_kwargs with cascade="all, delete-orphan")
- [ ] T015 [US1] Verify foreign key constraints are defined in models (Task.user_id, Conversation.user_id, Message.conversation_id)
- [ ] T016 [US1] Check model exports in backend/app/models/__init__.py (User, Task, Conversation, Message, MessageRole)

### Testing for User Story 1

- [ ] T017 [US1] Create validation script backend/tests/test_model_validation.py to verify model field types and constraints
- [ ] T018 [US1] Create test script backend/tests/test_relationships.py to validate relationships (Conversation → Message)
- [ ] T019 [US1] Create cascade delete test in backend/tests/test_cascade_delete.py (delete conversation, verify messages deleted)
- [ ] T020 [US1] Run test_model_validation.py and verify all assertions pass
- [ ] T021 [US1] Run test_relationships.py and verify relationship queries work correctly
- [ ] T022 [US1] Run test_cascade_delete.py and verify SC-008 (100% cascade deletion success)

**Checkpoint**: All models validated against specification, relationships tested, cascade deletion verified

---

## Phase 4: User Story 2 - Database Migration Management (Priority: P2)

**Goal**: Validate that Alembic migrations are properly configured, version-controlled, and can be applied/rolled back safely

**Independent Test**: Apply migrations to empty database, verify schema, rollback, verify schema reverted, re-apply

### Validation for User Story 2

- [ ] T023 [P] [US2] Review Alembic migrations in backend/alembic/versions/ directory for completeness (initial schema, conversations/messages addition)
- [ ] T024 [P] [US2] Verify alembic.ini in backend/ has correct sqlalchemy.url configuration (uses environment variable)
- [ ] T025 [P] [US2] Verify backend/alembic/env.py imports all models and sets target_metadata = SQLModel.metadata
- [ ] T026 [US2] Check migration upgrade functions create all tables (tasks, conversations, messages) with proper constraints
- [ ] T027 [US2] Check migration downgrade functions properly reverse schema changes

### Testing for User Story 2

- [ ] T028 [US2] Create test database for migration testing (separate from main DATABASE_URL)
- [ ] T029 [US2] Test migration apply with `alembic upgrade head` on test database and verify SC-010 (completes in <30 seconds)
- [ ] T030 [US2] Inspect database schema after migration using SQL queries to verify tables, indexes, constraints exist per SC-001
- [ ] T031 [US2] Test migration rollback with `alembic downgrade -1` and verify database state reverts correctly per SC-005
- [ ] T032 [US2] Test re-applying migration with `alembic upgrade head` to verify idempotency
- [ ] T033 [US2] Verify migration version tracking in alembic_version table shows correct current version

**Checkpoint**: Migration workflow validated, apply/rollback tested, version control verified

---

## Phase 5: User Story 3 - Secure Database Connection (Priority: P3)

**Goal**: Validate that application connects securely to Neon PostgreSQL with SSL, uses connection pooling, and handles concurrent sessions

**Independent Test**: Connect to Neon database, verify SSL encryption, test connection pool under load, measure query performance

### Validation for User Story 3

- [ ] T034 [P] [US3] Verify DATABASE_URL in backend/.env includes `?sslmode=require` parameter for Neon SSL
- [ ] T035 [P] [US3] Review backend/app/database.py engine configuration (pool_size=5, max_overflow=10, pool_pre_ping=True, pool_recycle=3600)
- [ ] T036 [P] [US3] Verify get_session() function in backend/app/database.py uses context manager for proper session cleanup
- [ ] T037 [US3] Check config.py in backend/app/config.py loads DATABASE_URL from environment with pydantic-settings

### Testing for User Story 3

- [ ] T038 [US3] Create SSL connection test backend/tests/test_ssl_connection.py to verify secure connection per SC-004
- [ ] T039 [US3] Create connection pool test backend/tests/test_connection_pool.py to verify pool manages 20 concurrent sessions per SC-006
- [ ] T040 [US3] Create performance test backend/tests/test_query_performance.py to verify user_id queries <50ms for 10K records per SC-003
- [ ] T041 [US3] Run test_ssl_connection.py and verify `SHOW ssl;` returns 'on' in PostgreSQL
- [ ] T042 [US3] Run test_connection_pool.py with 20 parallel requests and verify no pool timeout errors
- [ ] T043 [US3] Run test_query_performance.py with sample data and verify query time meets SC-003 requirement

**Checkpoint**: SSL connection verified, connection pooling tested under load, query performance validated

---

## Phase 6: Polish & Documentation

**Purpose**: Create comprehensive documentation and validation reports

- [ ] T044 [P] Create validation summary document in specs/014-database-models/VALIDATION_REPORT.md with test results for all success criteria (SC-001 through SC-010)
- [ ] T045 [P] Update backend/README.md with database setup instructions, migration workflow, and troubleshooting guide
- [ ] T046 [P] Create ER diagram image from data-model.md and save to specs/014-database-models/diagrams/entity-relationship.png
- [ ] T047 Document all discovered issues or deviations from specification in specs/014-database-models/ISSUES.md
- [ ] T048 Update constitution compliance report in specs/014-database-models/plan.md if any new findings during validation
- [ ] T049 Create quickstart video/GIF showing migration workflow (apply, inspect, rollback) and save to specs/014-database-models/assets/
- [ ] T050 Review and update all inline docstrings in backend/app/models/ files for completeness and accuracy

---

## Dependencies & Parallel Execution

### User Story Dependencies

```
US1 (Database Schema) ─────┐
                           ├──→ US2 (Migration Management)
                           │
                           └──→ US3 (Secure Connection)
```

**Explanation**:
- **US1 is foundational**: Models must be defined before migrations can manage them
- **US2 and US3 are independent**: Can validate migration workflow and connection settings in parallel after US1
- **All stories are independently testable**: Each has clear acceptance criteria from specification

### Parallel Execution Opportunities

**Phase 1 (Setup)**:
- T002, T003, T004 can run in parallel (different files)

**Phase 2 (Foundational)**:
- After T007 (DATABASE_URL configured), T008, T009, T010 can run in parallel

**Phase 3 (US1)**:
- T011, T012, T013 can run in parallel (validate different models)
- T017, T018, T019 can be created in parallel (different test files)

**Phase 4 (US2)**:
- T023, T024, T025 can run in parallel (review different migration files)

**Phase 5 (US3)**:
- T034, T035, T036, T037 can run in parallel (review different configuration aspects)
- T038, T039, T040 can be created in parallel (different test files)

**Phase 6 (Polish)**:
- T044, T045, T046, T047 can run in parallel (different documentation files)

### Sequential Dependencies

**Must complete in order**:
1. Phase 1 → Phase 2 (must review before setting up environment)
2. Phase 2 → Phase 3 (must have environment ready before validation)
3. Within US1: T011-T016 → T017-T019 (create tests) → T020-T022 (run tests)
4. Within US2: T023-T027 → T028-T033 (must review migrations before testing them)
5. Within US3: T034-T037 → T038-T043 (must review config before testing)

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)

**Recommended MVP**: User Story 1 only (Database Schema Definition)
- Validates core models are correctly defined
- Tests relationships and cascade deletion
- Confirms foundation is solid for all features

**Rationale**: US1 is foundational - all application features depend on properly defined models. Without validated models, migration management (US2) and connection testing (US3) are meaningless.

### Incremental Delivery

**Sprint 1** (MVP): US1 - Database Schema Definition
- Deliverable: Validated models with passing relationship tests
- Value: Confidence that data layer is correctly implemented

**Sprint 2**: US2 - Database Migration Management
- Deliverable: Verified migration workflow with apply/rollback tests
- Value: Safe schema evolution process for future changes

**Sprint 3**: US3 - Secure Database Connection
- Deliverable: Validated SSL connection, connection pooling, query performance
- Value: Production-ready database layer with security and performance guarantees

**Sprint 4**: Documentation & Polish
- Deliverable: Comprehensive validation report, updated documentation, ER diagrams
- Value: Knowledge transfer and maintenance readiness

### Testing Strategy

Since implementation already exists, focus on **validation testing** rather than TDD:

1. **Model Validation Tests** (US1): Verify field types, constraints, relationships against spec
2. **Migration Tests** (US2): Apply/rollback cycles on test database
3. **Connection Tests** (US3): SSL verification, pool stress testing, performance benchmarks
4. **Integration Tests**: End-to-end workflow (create conversation → add messages → delete conversation → verify cascade)

### Risk Mitigation

**Risk 1**: Existing models don't match specification
- **Mitigation**: T011-T016 will detect discrepancies early in Phase 3

**Risk 2**: Migrations are incomplete or incorrect
- **Mitigation**: T023-T027 review migrations before testing

**Risk 3**: Connection configuration doesn't meet performance goals
- **Mitigation**: T040-T043 measure actual performance against SC-003 requirement

---

## Success Criteria Verification Map

| Success Criterion | Verified By Task(s) | Phase |
|-------------------|---------------------|-------|
| SC-001: Schema matches model definitions (100%) | T030 | Phase 4 (US2) |
| SC-002: Foreign key relationships enforced | T015, T019 | Phase 3 (US1) |
| SC-003: Queries <50ms for 10K records | T040, T043 | Phase 5 (US3) |
| SC-004: SSL connections to Neon successful | T038, T041 | Phase 5 (US3) |
| SC-005: Migrations apply/rollback without data loss | T031 | Phase 4 (US2) |
| SC-006: Connection pool manages 20 concurrent sessions | T039, T042 | Phase 5 (US3) |
| SC-007: Timestamps auto-populated | T011, T012, T020 | Phase 3 (US1) |
| SC-008: Cascade deletion 100% success | T019, T022 | Phase 3 (US1) |
| SC-009: Indexes utilized by optimizer | T030, T043 | Phase 4 & 5 |
| SC-010: Migration <30 seconds | T029 | Phase 4 (US2) |

---

## Task Summary

**Total Tasks**: 50
- **Phase 1 (Setup)**: 5 tasks
- **Phase 2 (Foundational)**: 5 tasks
- **Phase 3 (US1 - Schema)**: 12 tasks
- **Phase 4 (US2 - Migrations)**: 11 tasks
- **Phase 5 (US3 - Connection)**: 10 tasks
- **Phase 6 (Polish)**: 7 tasks

**Parallel Opportunities**: 19 tasks marked with [P] can run in parallel

**User Story Distribution**:
- US1 (P1 - Database Schema): 12 tasks
- US2 (P2 - Migration Management): 11 tasks
- US3 (P3 - Secure Connection): 10 tasks
- Setup/Foundation: 10 tasks
- Polish: 7 tasks

**Estimated Effort**:
- Phase 1-2: 2-3 hours (environment setup and review)
- Phase 3 (US1): 4-6 hours (model validation and relationship testing)
- Phase 4 (US2): 3-4 hours (migration workflow testing)
- Phase 5 (US3): 3-4 hours (connection and performance testing)
- Phase 6: 2-3 hours (documentation)
- **Total**: 14-20 hours for comprehensive validation

**Format Validation**: ✅ All tasks follow required checklist format with checkbox, ID, optional [P] and [Story] labels, and specific file paths.

---

## Next Steps

1. Start with **Phase 1** to review existing implementation
2. Setup test environment in **Phase 2**
3. Begin **Phase 3 (US1)** for MVP - validate core models
4. Once US1 passes, proceed to **Phase 4 (US2)** and **Phase 5 (US3)** in parallel
5. Complete **Phase 6** to document findings and create validation report

**Remember**: Implementation already exists. Focus is on thorough validation that existing code meets all specification requirements (FR-001 through FR-015) and success criteria (SC-001 through SC-010).
