#!/bin/bash

echo "=================================="
echo "Chat Feature Quick Verification"
echo "=================================="
echo ""

# Check if backend is running
echo "1. Checking backend health..."
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo "   ✅ Backend is running"
else
    echo "   ❌ Backend is NOT running"
    echo "   Start it with: cd backend && ./venv/Scripts/python.exe -m uvicorn app.main:app --reload"
    exit 1
fi

# Check if frontend build works
echo ""
echo "2. Checking frontend build..."
cd /mnt/d/todo-fullstack-web/frontend
if npm run build > /dev/null 2>&1; then
    echo "   ✅ Frontend builds successfully"
else
    echo "   ❌ Frontend build failed"
    exit 1
fi

# Check TypeScript
echo ""
echo "3. Checking TypeScript..."
if npx tsc --noEmit > /dev/null 2>&1; then
    echo "   ✅ No TypeScript errors"
else
    echo "   ❌ TypeScript errors found"
    exit 1
fi

echo ""
echo "=================================="
echo "✅ All checks passed!"
echo "=================================="
echo ""
echo "To use the chat feature:"
echo "1. Go to http://localhost:3000/signin"
echo "2. Sign in with your credentials"
echo "3. Click 'Perform Tasks With AI' button"
echo "4. Start chatting!"
echo ""
echo "See CHAT_FEATURE_USAGE_GUIDE.md for detailed instructions"
