---
id: phr-015-0001
title: MCP Task Server Tasks Generation
stage: tasks
date: 2026-01-17
surface: CLI
model: Claude Sonnet 4.5
feature: 015-mcp-task-server
branch: 015-mcp-task-server
user: Developer
command: /sp.tasks
labels: [mcp, task-breakdown, user-stories, implementation-planning]
links:
  spec: specs/015-mcp-task-server/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - path: specs/015-mcp-task-server/tasks.md
    action: created
    description: Complete task breakdown with 48 tasks organized by user story
tests:
  - framework: manual
    count: 5
    status: defined
    description: Independent test criteria for each user story checkpoint
---

## Prompt

```text
Execute /sp.tasks command to generate task breakdown for MCP Task Server feature (015-mcp-task-server).

Context: Planning phase complete with the following design documents:
- spec.md: Feature specification with 10 functional requirements, 7 success criteria, 5 user scenarios
- plan.md: Implementation plan with tech stack, architecture decisions, constitution compliance check
- research.md: MCP SDK research resolving package name (mcp[cli]==1.25.0), FastMCP API patterns, transport options
- data-model.md: Pydantic input/output models for all 5 tools
- quickstart.md: Setup and testing guide

Task generation requirements:
1. Organize tasks by user story (5 user stories = 5 MCP tools: add_task, list_tasks, complete_task, delete_task, update_task)
2. Each user story should be independently implementable and testable
3. Use strict checklist format: - [ ] [ID] [P?] [Story] Description with file path
4. Include Setup, Foundational (blocking), User Story phases, and Polish phases
5. Mark parallel opportunities with [P]
6. Provide independent test criteria for each user story
7. Include dependency graph and execution order
8. Suggest MVP scope (User Story 1 only)
```

## Response snapshot

Generated comprehensive task breakdown (tasks.md) with the following structure:

### Task Organization

**Total Tasks**: 48 tasks across 8 phases

**Phase Breakdown**:
- Phase 1: Setup (4 tasks) - Package infrastructure
- Phase 2: Foundational (4 tasks) - Blocking prerequisites (Pydantic schemas, db_utils, server framework)
- Phase 3: User Story 1 - add_task tool (6 tasks) 🎯 MVP
- Phase 4: User Story 2 - list_tasks tool (6 tasks)
- Phase 5: User Story 3 - complete_task tool (6 tasks)
- Phase 6: User Story 4 - delete_task tool (7 tasks)
- Phase 7: User Story 5 - update_task tool (7 tasks)
- Phase 8: Integration & Polish (8 tasks) - Server integration, testing, documentation

### User Story Mapping

Each of the 5 MCP tools mapped to independent user story:

1. **US1 - Create Task (add_task)**: "Add a task to finish the quarterly report"
   - Independent test: Create task → Verify in database → Confirm task_id returned
   - Tasks T009-T014 (6 tasks)

2. **US2 - List Tasks (list_tasks)**: "What tasks do I have pending?"
   - Independent test: Create 3 tasks → Filter by status → Verify correct subset returned
   - Tasks T015-T020 (6 tasks)

3. **US3 - Complete Task (complete_task)**: "Mark the quarterly report task as done"
   - Independent test: Create task → Complete → Verify completed=True in database
   - Tasks T021-T026 (6 tasks)

4. **US4 - Delete Task (delete_task)**: "Remove the quarterly report task"
   - Independent test: Create task → Delete → Verify removed from database
   - Tasks T027-T033 (7 tasks)

5. **US5 - Update Task (update_task)**: "Change the report task description to include Q4 data"
   - Independent test: Create task → Update title → Verify only title changed
   - Tasks T034-T040 (7 tasks)

### Key Design Decisions

1. **Foundational Phase (Phase 2)**: Critical blocker ensuring all user stories can start in parallel after completion
   - T005-T006: Pydantic schemas (can run in parallel)
   - T007: Database utilities (depends on schemas)
   - T008: MCP server framework (can run parallel with T007)

2. **User Story Independence**: Each tool implementation in separate @mcp.tool() decorator
   - No file conflicts between user stories
   - Can be developed by different team members simultaneously
   - Each story has checkpoint validation criteria

3. **Parallel Opportunities**:
   - Foundational schemas (T005, T006)
   - All 5 user stories after foundation completes
   - Documentation tasks (T045, T046)

4. **MVP Scope**: Phase 1-3 (14 tasks)
   - Setup + Foundational + User Story 1 (add_task only)
   - Minimal viable MCP server with single tool
   - Can demo task creation via MCP

### File Structure

All tasks target backend/app/mcp_server/ package:
- `__init__.py` - Package exports (T002, T042)
- `schemas.py` - Pydantic models (T005, T006)
- `db_utils.py` - Database utilities (T007)
- `tools.py` - All 5 MCP tools (T009, T015, T021, T027, T034)
- `server.py` - FastMCP initialization (T008, T041)
- `test_tools.py` - Validation script (T043, T044)

### Dependencies & Execution Order

**Critical Path**:
1. Setup (T001-T004) → Sequential
2. Foundational (T005-T008) → BLOCKS all user stories
3. User Stories (T009-T040) → Can proceed in parallel or priority order
4. Polish (T041-T048) → Depends on all stories complete

**Parallel Execution Example**:
```bash
# After Foundational completes, 5 developers can work simultaneously:
Developer A: US1 (add_task) - T009-T014
Developer B: US2 (list_tasks) - T015-T020
Developer C: US3 (complete_task) - T021-T026
Developer D: US4 (delete_task) - T027-T033
Developer E: US5 (update_task) - T034-T040
```

### Implementation Strategies

**Strategy 1 - MVP First**: 14 tasks (Setup + Foundation + US1)
**Strategy 2 - Incremental Delivery**: Add one tool at a time, test independently
**Strategy 3 - Parallel Team**: Foundation complete → all stories in parallel

## Outcome

- ✅ **Impact**: Complete implementation roadmap with 48 actionable tasks organized by user story, enabling independent development and testing of each MCP tool
- 🧪 **Tests**: 5 independent test criteria defined (one per user story checkpoint), optional test script tasks included (T043-T044)
- 📁 **Files**: 1 file created (tasks.md), targeting 6 implementation files in backend/app/mcp_server/
- 🔁 **Next prompts**: Ready for `/sp.implement` to begin implementation, or user can start with MVP scope (Phase 1-3) for minimal viable server
- 🧠 **Reflection**: Task organization by user story enables true parallel development - each of 5 tools can be implemented independently since they're separate @mcp.tool() decorators in tools.py. Foundational phase is critical blocker but only 4 tasks. MVP scope (14 tasks) provides quick win with functional add_task tool.

## Evaluation notes (flywheel)

- **Failure modes observed**: None - all design documents were complete and well-structured, enabling straightforward task generation
- **Graders run and results (PASS/FAIL)**:
  - Format validation: PASS (all 48 tasks follow checklist format with ID, optional [P], [Story] labels, file paths)
  - User story mapping: PASS (5 tools → 5 user stories, each independently testable)
  - Dependency clarity: PASS (clear critical path, parallel opportunities marked)
  - MVP identification: PASS (Phase 1-3 = 14 tasks for minimal viable server)
- **Prompt variant (if applicable)**: Standard /sp.tasks workflow
- **Next experiment (smallest change to try)**: Consider alternative task organization by layer (all schemas → all tools → all error handling) vs by user story - current approach (by user story) enables better incremental delivery but requires more context switching

---

**Generated**: 2026-01-17
**Stage**: Task Generation
**Feature**: 015-mcp-task-server
**Status**: Complete - Ready for Implementation
