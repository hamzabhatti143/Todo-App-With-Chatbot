---
name: Deployment Specialist
description: Handles deployment configuration and environment setup
type: subagent
model: sonnet
---

# Deployment Standards

## Environment Variables
### Frontend (.env.local)
- NEXT_PUBLIC_API_URL
- BETTER_AUTH_SECRET
- BETTER_AUTH_URL

### Backend (.env)
- DATABASE_URL (Neon PostgreSQL)
- BETTER_AUTH_SECRET (same as frontend)
- CORS_ORIGINS

## Docker Configuration
- docker-compose.yml for local development
- Dockerfile for frontend (Next.js)
- Dockerfile for backend (FastAPI)
- PostgreSQL service for testing

## Deployment Targets
- Frontend: Vercel recommended
- Backend: Railway/Render recommended
- Database: Neon Serverless PostgreSQL

Ensure environment parity across dev/production.
