---
name: JWT Auth Workflow
description: Auto-handle JWT authentication integration
trigger: When implementing auth-protected features
auto_invoke: true
---

# JWT Auth Workflow Skill

Auto-handles:
- JWT token inclusion in frontend requests
- JWT verification in backend routes
- User ID extraction and validation
- Auth error handling

## Frontend Auth Flow
1. User logs in → Better Auth issues JWT
2. Token stored securely
3. API client includes token in headers:
   Authorization: Bearer <token>

## Backend Auth Flow
1. Extract token from Authorization header
2. Verify signature with BETTER_AUTH_SECRET
3. Decode to get user_id
4. Match with URL user_id parameter
5. Return 401 if invalid

## Shared Secret
Both frontend and backend must use same:
BETTER_AUTH_SECRET environment variable

Auto-enforce auth on all protected routes.
