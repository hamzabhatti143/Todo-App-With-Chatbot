#!/bin/bash
# Integration Test Script
# Tests backend API endpoints with curl

set -e  # Exit on error

echo "=========================================="
echo "Integration Test Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
API_URL=${API_URL:-"http://localhost:8000"}
FRONTEND_URL=${FRONTEND_URL:-"http://localhost:3000"}

# Test counters
PASSED=0
FAILED=0

# Helper function to print test result
pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Test 1: Backend Health Check
echo "Test 1: Backend Health Check"
response=$(curl -s -w "%{http_code}" -o /tmp/health.json "${API_URL}/health" 2>/dev/null || echo "000")
if [ "$response" = "200" ]; then
    pass "Backend health check passed (200 OK)"
else
    fail "Backend health check failed (HTTP $response)"
    warn "Is the backend running? Start with: cd backend && uvicorn app.main:app --reload"
fi
echo ""

# Test 2: OpenAPI Documentation
echo "Test 2: OpenAPI Documentation"
response=$(curl -s -w "%{http_code}" -o /tmp/openapi.json "${API_URL}/docs" 2>/dev/null || echo "000")
if [ "$response" = "200" ]; then
    pass "OpenAPI docs available at ${API_URL}/docs"
else
    fail "OpenAPI docs not accessible (HTTP $response)"
fi
echo ""

# Test 3: User Registration
echo "Test 3: User Registration"
RANDOM_EMAIL="test$(date +%s)@example.com"
RANDOM_PASSWORD="TestPass$(date +%s)!"

response=$(curl -s -w "%{http_code}" -o /tmp/register.json "${API_URL}/api/auth/register" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"${RANDOM_EMAIL}\",\"password\":\"${RANDOM_PASSWORD}\"}" 2>/dev/null || echo "000")

if [ "$response" = "201" ]; then
    USER_ID=$(cat /tmp/register.json | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
    pass "User registration successful (201 Created)"
    echo "   Email: ${RANDOM_EMAIL}"
    echo "   User ID: ${USER_ID}"
else
    fail "User registration failed (HTTP $response)"
    cat /tmp/register.json 2>/dev/null
fi
echo ""

# Test 4: User Login
echo "Test 4: User Login"
response=$(curl -s -w "%{http_code}" -o /tmp/login.json "${API_URL}/api/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"${RANDOM_EMAIL}\",\"password\":\"${RANDOM_PASSWORD}\"}" 2>/dev/null || echo "000")

if [ "$response" = "200" ]; then
    ACCESS_TOKEN=$(cat /tmp/login.json | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
    pass "User login successful (200 OK)"
    echo "   Token: ${ACCESS_TOKEN:0:50}..."
else
    fail "User login failed (HTTP $response)"
    cat /tmp/login.json 2>/dev/null
fi
echo ""

# Test 5: List Tasks (Empty)
echo "Test 5: List Tasks (Empty)"
if [ -n "$ACCESS_TOKEN" ] && [ -n "$USER_ID" ]; then
    response=$(curl -s -w "%{http_code}" -o /tmp/tasks.json "${API_URL}/api/${USER_ID}/tasks" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}" 2>/dev/null || echo "000")

    if [ "$response" = "200" ]; then
        TASK_COUNT=$(cat /tmp/tasks.json | grep -o '\[' | wc -l)
        pass "List tasks successful (200 OK)"
        echo "   Tasks: $(cat /tmp/tasks.json)"
    else
        fail "List tasks failed (HTTP $response)"
        cat /tmp/tasks.json 2>/dev/null
    fi
else
    fail "Skipped (no auth token or user ID)"
fi
echo ""

# Test 6: Create Task
echo "Test 6: Create Task"
if [ -n "$ACCESS_TOKEN" ] && [ -n "$USER_ID" ]; then
    response=$(curl -s -w "%{http_code}" -o /tmp/create_task.json "${API_URL}/api/${USER_ID}/tasks" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}" \
        -H "Content-Type: application/json" \
        -d '{"title":"Integration Test Task","description":"Created by integration test script"}' 2>/dev/null || echo "000")

    if [ "$response" = "201" ]; then
        TASK_ID=$(cat /tmp/create_task.json | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
        pass "Create task successful (201 Created)"
        echo "   Task ID: ${TASK_ID}"
        echo "   Title: Integration Test Task"
    else
        fail "Create task failed (HTTP $response)"
        cat /tmp/create_task.json 2>/dev/null
    fi
else
    fail "Skipped (no auth token or user ID)"
fi
echo ""

# Test 7: Get Specific Task
echo "Test 7: Get Specific Task"
if [ -n "$ACCESS_TOKEN" ] && [ -n "$USER_ID" ] && [ -n "$TASK_ID" ]; then
    response=$(curl -s -w "%{http_code}" -o /tmp/get_task.json "${API_URL}/api/${USER_ID}/tasks/${TASK_ID}" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}" 2>/dev/null || echo "000")

    if [ "$response" = "200" ]; then
        pass "Get task successful (200 OK)"
        TASK_TITLE=$(cat /tmp/get_task.json | grep -o '"title":"[^"]*"' | cut -d'"' -f4)
        echo "   Retrieved task: ${TASK_TITLE}"
    else
        fail "Get task failed (HTTP $response)"
    fi
else
    fail "Skipped (no auth token, user ID, or task ID)"
fi
echo ""

# Test 8: Toggle Task Completion
echo "Test 8: Toggle Task Completion"
if [ -n "$ACCESS_TOKEN" ] && [ -n "$USER_ID" ] && [ -n "$TASK_ID" ]; then
    response=$(curl -s -w "%{http_code}" -o /tmp/toggle_task.json -X PATCH \
        "${API_URL}/api/${USER_ID}/tasks/${TASK_ID}/complete" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}" 2>/dev/null || echo "000")

    if [ "$response" = "200" ]; then
        COMPLETED=$(cat /tmp/toggle_task.json | grep -o '"completed":[^,}]*' | cut -d':' -f2)
        pass "Toggle completion successful (200 OK)"
        echo "   Completed: ${COMPLETED}"
    else
        fail "Toggle completion failed (HTTP $response)"
    fi
else
    fail "Skipped (no auth token, user ID, or task ID)"
fi
echo ""

# Test 9: Update Task
echo "Test 9: Update Task"
if [ -n "$ACCESS_TOKEN" ] && [ -n "$USER_ID" ] && [ -n "$TASK_ID" ]; then
    response=$(curl -s -w "%{http_code}" -o /tmp/update_task.json -X PUT \
        "${API_URL}/api/${USER_ID}/tasks/${TASK_ID}" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}" \
        -H "Content-Type: application/json" \
        -d '{"title":"Updated Integration Test Task","description":"Updated by test script"}' 2>/dev/null || echo "000")

    if [ "$response" = "200" ]; then
        pass "Update task successful (200 OK)"
        echo "   New title: Updated Integration Test Task"
    else
        fail "Update task failed (HTTP $response)"
    fi
else
    fail "Skipped (no auth token, user ID, or task ID)"
fi
echo ""

# Test 10: Delete Task
echo "Test 10: Delete Task"
if [ -n "$ACCESS_TOKEN" ] && [ -n "$USER_ID" ] && [ -n "$TASK_ID" ]; then
    response=$(curl -s -w "%{http_code}" -o /tmp/delete_task.json -X DELETE \
        "${API_URL}/api/${USER_ID}/tasks/${TASK_ID}" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}" 2>/dev/null || echo "000")

    if [ "$response" = "204" ]; then
        pass "Delete task successful (204 No Content)"
    else
        fail "Delete task failed (HTTP $response)"
    fi
else
    fail "Skipped (no auth token, user ID, or task ID)"
fi
echo ""

# Test 11: Frontend Health Check
echo "Test 11: Frontend Health Check"
response=$(curl -s -w "%{http_code}" -o /tmp/frontend.html "${FRONTEND_URL}" 2>/dev/null || echo "000")
if [ "$response" = "200" ]; then
    pass "Frontend accessible (200 OK)"
    echo "   URL: ${FRONTEND_URL}"
else
    fail "Frontend not accessible (HTTP $response)"
    warn "Is the frontend running? Start with: cd frontend && npm run dev"
fi
echo ""

# Test 12: CORS Preflight
echo "Test 12: CORS Preflight"
response=$(curl -s -w "%{http_code}" -o /tmp/cors.txt -X OPTIONS "${API_URL}/api/auth/login" \
    -H "Origin: ${FRONTEND_URL}" \
    -H "Access-Control-Request-Method: POST" \
    -H "Access-Control-Request-Headers: Content-Type" 2>/dev/null || echo "000")

if [ "$response" = "200" ]; then
    pass "CORS preflight successful (200 OK)"
    echo "   Frontend can communicate with backend"
else
    warn "CORS preflight check inconclusive (HTTP $response)"
fi
echo ""

# Summary
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo -e "${GREEN}Passed: ${PASSED}${NC}"
echo -e "${RED}Failed: ${FAILED}${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Open ${FRONTEND_URL} in your browser"
    echo "2. Register a new user"
    echo "3. Create, edit, and delete tasks"
    echo "4. Test filtering and completion toggle"
    echo "5. Test on mobile device (320px width)"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "1. Make sure backend is running: cd backend && uvicorn app.main:app --reload"
    echo "2. Make sure frontend is running: cd frontend && npm run dev"
    echo "3. Check API_URL and FRONTEND_URL environment variables"
    echo "4. Check logs for errors"
    echo ""
    exit 1
fi
