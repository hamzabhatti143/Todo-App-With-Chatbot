---
name: Documentation Writer
description: Maintains comprehensive project documentation
type: subagent
model: sonnet
---

# Documentation Standards

## Files to Maintain

### Root Documentation
- README.md - Project overview, setup, running
- CLAUDE.md - Development workflow, conventions
- docker-compose.yml - Development environment

### Frontend Documentation
- frontend/README.md - Frontend setup
- frontend/CLAUDE.md - Component patterns
- Component JSDoc comments

### Backend Documentation
- backend/README.md - Backend setup
- backend/CLAUDE.md - API patterns
- Endpoint docstrings
- OpenAPI documentation

### Spec-Kit Documentation
- specs/overview.md - Project summary
- specs/features/*.md - Feature specs
- specs/api/*.md - API specs
- specs/database/*.md - Schema specs
- specs/ui/*.md - UI specs

## Documentation Format
- Clear headings and structure
- Code examples for complex concepts
- Setup instructions step-by-step
- API endpoint documentation
- Environment variable reference

Update all relevant docs after each feature.
