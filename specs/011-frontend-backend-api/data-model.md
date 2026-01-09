# Data Model: Frontend-Backend API Communication Verification

**Feature**: 011-frontend-backend-api
**Date**: 2026-01-01

## Overview

This feature focuses on verification and testing infrastructure rather than data persistence. The data model describes the runtime data structures used for testing and displaying integration status.

## Entities

### 1. Health Check Response

**Purpose**: Represents the backend health status response

**Attributes**:
- `status`: string - Health status indicator (e.g., "ok", "healthy")

**Validation Rules**:
- `status` must be a non-empty string
- Response must be valid JSON

**State**:
- Stateless - no persistence required
- Transient data displayed in UI

**Relationships**:
- None - standalone response entity

**Example**:
```json
{
  "status": "ok"
}
```

---

### 2. Registration Request

**Purpose**: User registration data sent from frontend to backend

**Attributes**:
- `email`: string - User email address
- `password`: string - User password (plain text, hashed on backend)

**Validation Rules**:
- `email`: Valid email format, max 255 characters
- `password`: Minimum 8 characters (configurable)
- Both fields required

**Security**:
- Password transmitted over HTTPS only
- Password hashed with bcrypt on backend before storage
- Never logged or displayed

**Example**:
```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

---

### 3. Registration Response

**Purpose**: Confirmation of successful user registration

**Attributes**:
- `id`: UUID - Unique user identifier
- `email`: string - Registered email address
- `created_at`: ISO 8601 timestamp - Account creation time
- `updated_at`: ISO 8601 timestamp - Last update time

**Validation Rules**:
- `id`: Valid UUID format
- `email`: Matches registration request email
- `created_at`, `updated_at`: Valid ISO 8601 timestamps
- Password MUST NOT be included in response (security)

**Example**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "test@example.com",
  "created_at": "2026-01-01T09:00:00Z",
  "updated_at": "2026-01-01T09:00:00Z"
}
```

---

### 4. Login Request

**Purpose**: Authentication credentials for login

**Attributes**:
- `email`: string - User email address
- `password`: string - User password (plain text)

**Validation Rules**:
- `email`: Valid email format
- `password`: Non-empty string
- Both fields required

**Security**:
- Transmitted over HTTPS only
- Password compared against hashed version in database
- Failed login attempts should not reveal if email exists

**Example**:
```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

---

### 5. Login Response (JWT Token)

**Purpose**: Authentication token for authorized requests

**Attributes**:
- `access_token`: string - JWT token
- `token_type`: string - Token type (always "bearer")

**Validation Rules**:
- `access_token`: Valid JWT format (3 parts separated by dots)
- `token_type`: Must be "bearer"

**Token Structure** (JWT payload):
- `sub`: User ID (UUID string)
- `exp`: Expiration timestamp
- `iat`: Issued at timestamp

**Security**:
- Token signed with `BETTER_AUTH_SECRET`
- Token expires after configured time (default 30 minutes)
- Token must be validated on all protected endpoints

**Example**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJleHAiOjE3MDY3Nzg2MDB9.signature",
  "token_type": "bearer"
}
```

---

### 6. Frontend Test State

**Purpose**: UI state for tracking test results

**Attributes**:
- `health`: object | null - Health check response or null
- `error`: string - Error message or empty string
- `testing`: boolean - Loading state during API call
- `authResult`: object | null - Authentication test result
- `authError`: string - Authentication error message
- `authTesting`: boolean - Auth test loading state
- `testEmail`: string - Email input value
- `testPassword`: string - Password input value

**State Transitions**:
```
Initial → Testing → Success | Error
  ↓         ↓          ↓        ↓
 Idle → Loading → Display | Display
```

**Validation**:
- All states managed via React useState
- State updates trigger UI re-renders
- Error and success states mutually exclusive

---

## Data Flow Diagrams

### Health Check Flow

```
Frontend                    Backend
   |                           |
   |-- GET /health ----------->|
   |                           |
   |                    [Verify server]
   |                           |
   |<- 200 {status:"ok"} ------|
   |                           |
[Display success]              |
```

### Registration Flow

```
Frontend                    Backend                    Database
   |                           |                           |
   |-- POST /auth/register --->|                           |
   |   {email, password}       |                           |
   |                           |-- Hash password           |
   |                           |                           |
   |                           |-- INSERT user ----------->|
   |                           |                           |
   |                           |<- user record ------------|
   |                           |                           |
   |<- 201 {id, email, ...} ---|                           |
   |                           |                           |
[Display success + data]      |                           |
```

### Login Flow

```
Frontend                    Backend                    Database
   |                           |                           |
   |-- POST /auth/login ------>|                           |
   |   {email, password}       |                           |
   |                           |-- SELECT user ----------->|
   |                           |                           |
   |                           |<- user record ------------|
   |                           |                           |
   |                           |-- Verify password         |
   |                           |-- Generate JWT            |
   |                           |                           |
   |<- 200 {access_token} -----|                           |
   |                           |                           |
[Store token, display]        |                           |
```

---

## Validation Rules Summary

| Entity | Field | Type | Required | Constraints |
|--------|-------|------|----------|-------------|
| Health Response | status | string | Yes | Non-empty |
| Registration Request | email | string | Yes | Valid email, max 255 chars |
| Registration Request | password | string | Yes | Min 8 chars |
| Registration Response | id | UUID | Yes | Valid UUID |
| Registration Response | email | string | Yes | Matches request |
| Registration Response | created_at | timestamp | Yes | ISO 8601 |
| Login Request | email | string | Yes | Valid email |
| Login Request | password | string | Yes | Non-empty |
| Login Response | access_token | string | Yes | Valid JWT |
| Login Response | token_type | string | Yes | "bearer" |

---

## Security Considerations

### Password Handling
- **Frontend**: Never store passwords, clear after submission
- **Transit**: HTTPS only, no logging
- **Backend**: Hash with bcrypt (cost factor 12) before storage
- **Database**: Only hashed passwords stored, never plain text

### JWT Token Handling
- **Frontend**: Store in localStorage or httpOnly cookies
- **Transit**: Include in `Authorization: Bearer <token>` header
- **Backend**: Verify signature with `BETTER_AUTH_SECRET`
- **Expiration**: Enforce token expiry, reject expired tokens

### CORS Configuration
- **Allowed Origins**: Whitelist only (http://localhost:3000)
- **Credentials**: Enabled for future authenticated requests
- **Methods**: All HTTP methods allowed for development
- **Headers**: All headers allowed for development

---

## Error Responses

### Backend Error Format

All backend errors follow this structure:

```json
{
  "detail": "Human-readable error message"
}
```

**Common Status Codes**:
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Authentication failed
- `403 Forbidden`: Authorization failed
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

**Example Error**:
```json
{
  "detail": "User with this email already exists"
}
```

---

## Implementation Notes

### Frontend State Management
- Use React `useState` for all test state
- Clear error states before new test
- Show loading states during API calls
- Display results in color-coded UI (green/red)

### Backend Response Format
- Always return JSON
- Include proper HTTP status codes
- Use FastAPI's automatic validation
- Never expose sensitive data (passwords, full tokens)

### Testing Validation
- Verify response structure matches expected format
- Check HTTP status codes
- Validate CORS headers present
- Confirm JWT token structure (header.payload.signature)

---

## References

- Backend models: `backend/app/models/user.py`
- Backend schemas: `backend/app/schemas/user.py`
- Frontend types: `frontend/types/auth.ts` (if created)
- API contracts: `specs/011-frontend-backend-api/contracts/`
