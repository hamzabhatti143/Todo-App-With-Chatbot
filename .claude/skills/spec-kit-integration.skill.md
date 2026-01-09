---
name: Spec-Kit Integration
description: Auto-reference and update Spec-Kit specifications
trigger: When implementing features or making changes
auto_invoke: true
---

# Spec-Kit Integration Skill

Auto-manages:
- Reading relevant specs before implementation
- Updating specs when requirements change
- Maintaining spec organization

## Spec Organization
specs/
├── overview.md          # Project overview
├── features/           # Feature specifications
├── api/                # API endpoint specs
├── database/           # Database schema specs
└── ui/                 # UI component specs

## Workflow
1. Read: @specs/features/[feature].md
2. Implement in frontend and backend
3. Update spec if changes needed
4. Reference in CLAUDE.md

Always keep specs in sync with implementation.
