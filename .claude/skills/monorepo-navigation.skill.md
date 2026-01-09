---
name: Monorepo Navigation
description: Auto-navigate monorepo structure
trigger: When working across frontend and backend
auto_invoke: true
---

# Monorepo Navigation Skill

Auto-activates when:
- Implementing features across multiple layers
- Referencing specs in /specs folder
- Working on frontend and backend simultaneously

## Navigation Patterns

### Reference Specs
@specs/features/task-crud.md
@specs/api/rest-endpoints.md
@specs/database/schema.md

### Frontend Work
cd frontend
npm run dev

### Backend Work
cd backend
uvicorn app.main:app --reload

### Full Stack
docker-compose up

Always maintain context of full stack architecture.
