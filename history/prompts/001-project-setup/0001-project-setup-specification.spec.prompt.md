---
id: 0001
title: Project Setup Specification
stage: spec
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5
feature: 001-project-setup
branch: 001-project-setup
user: system
command: /sp.specify
labels: ["spec", "project-setup", "monorepo", "infrastructure"]
links:
  spec: specs/001-project-setup/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-project-setup/spec.md
  - specs/001-project-setup/checklists/requirements.md
tests:
  - Specification quality checklist (all items passed)
---

## Prompt

Project Setup and Architecture for Full-Stack Todo Web Application

**Feature Name:** Project Setup and Monorepo Architecture

**Overview:**
Set up monorepo structure with Next.js 16+ frontend and FastAPI backend, configured for development with Docker Compose.

**Requirements:**

**1. Monorepo Structure:**
todo-fullstack-web/
├── .claude/                  # Already created
├── .spec-kit/
│   └── config.yaml
├── specs/                    # Already created
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   ├── lib/
│   │   ├── api.ts
│   │   └── auth.ts
│   ├── types/
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   ├── .env.example
│   ├── CLAUDE.md
│   └── README.md
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   ├── auth.py
│   │   ├── dependencies.py
│   │   └── routes/
│   ├── alembic/
│   ├── requirements.txt
│   ├── .env.example
│   ├── CLAUDE.md
│   └── README.md
├── docker-compose.yml
├── .gitignore
├── CLAUDE.md               # Already created
└── README.md

**2. Frontend Setup (Next.js 16+):**
- Initialize with: `npx create-next-app@latest frontend --typescript --tailwind --app`
- Install dependencies:
  - better-auth (authentication)
  - zod (validation)
  - axios (API client)
- Configure TypeScript strict mode
- Configure Tailwind CSS with custom theme
- Create .env.example with:
  - NEXT_PUBLIC_API_URL=http://localhost:8000
  - BETTER_AUTH_SECRET=
  - BETTER_AUTH_URL=http://localhost:3000

**3. Backend Setup (FastAPI):**
- Create requirements.txt with:
  - fastapi
  - uvicorn[standard]
  - sqlmodel
  - psycopg2-binary
  - python-jose[cryptography] (JWT)
  - python-multipart
  - alembic
  - python-dotenv
- Create .env.example with:
  - DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
  - BETTER_AUTH_SECRET=
  - CORS_ORIGINS=http://localhost:3000

**4. Spec-Kit Configuration:**
Create .spec-kit/config.yaml with structure definitions

**5. Docker Compose Configuration:**
Define frontend, backend, and PostgreSQL services

**6. Git Configuration:**
Create .gitignore for node_modules, .env, __pycache__, etc.

**Acceptance Criteria:**
- Monorepo structure created correctly
- Frontend initialized with Next.js 16+ App Router
- Backend initialized with FastAPI structure
- Dependencies installed
- Docker Compose runs all services
- All services accessible on correct ports
- Environment examples created
- Documentation files created

## Response snapshot

Created comprehensive feature specification for Project Setup and Monorepo Architecture with:

**4 Prioritized User Stories:**
1. Developer Environment Setup (P1) - Foundation for all development
2. Frontend Development Workflow (P2) - UI/UX development capability
3. Backend Development Workflow (P2) - API development capability
4. Full-Stack Integration Testing (P3) - End-to-end validation

**20 Functional Requirements:**
- Next.js 16+ with App Router and TypeScript strict mode
- FastAPI with Python 3.11+ and type hints
- PostgreSQL 15+ database
- Docker Compose for local development
- Better Auth with JWT for authentication
- Centralized API client and CORS configuration
- Auto-reload for both frontend and backend
- Complete documentation (README.md, CLAUDE.md)

**10 Success Criteria:**
- 10-minute setup time from clone to running
- Sub-2-second hot reload for both frontend and backend
- Zero configuration beyond .env file
- 100% environment variable documentation
- Full service integration via Docker Compose

**Quality Validation:**
All checklist items passed:
✅ No implementation details in user stories
✅ Technology-agnostic success criteria
✅ Zero [NEEDS CLARIFICATION] markers
✅ All requirements testable and unambiguous

## Outcome

- ✅ Impact: Feature specification created for foundational project setup, enables all subsequent development work
- 🧪 Tests: Specification quality checklist passed all validation items
- 📁 Files: Created spec.md and checklists/requirements.md in specs/001-project-setup/
- 🔁 Next prompts: /sp.plan to generate implementation plan for project setup
- 🧠 Reflection: Specification successfully captures infrastructure setup as user-centric stories, maintains technology-agnostic success criteria while documenting technical assumptions separately

## Evaluation notes (flywheel)

- Failure modes observed: None - specification complete with no clarifications needed
- Graders run and results (PASS/FAIL): PASS - All quality checklist items validated successfully
- Prompt variant (if applicable): Standard /sp.specify with detailed technical requirements
- Next experiment (smallest change to try): Monitor if setup user stories translate effectively to implementation tasks in /sp.plan phase
