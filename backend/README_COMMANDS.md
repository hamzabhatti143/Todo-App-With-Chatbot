# TodoBot Command & Usage Documentation

**Complete Guide to Using TodoBot for Task Management**

---

## 📚 Available Guides

This directory contains comprehensive documentation for using TodoBot:

### 1. **TODOBOT_COMMAND_GUIDE.md** 📖
   - **Purpose**: Complete command reference with examples
   - **Covers**: All operations (add, list, update, complete, delete)
   - **Best for**: Learning all available commands
   - **Length**: Comprehensive (detailed examples and explanations)

### 2. **QUICK_REFERENCE.md** ⚡
   - **Purpose**: Fast lookup for common commands
   - **Covers**: Essential commands and patterns
   - **Best for**: Quick reference while using TodoBot
   - **Length**: Concise (1-page cheat sheet)

### 3. **API_TESTING_GUIDE.md** 🧪
   - **Purpose**: Testing the chat endpoint with curl/Postman
   - **Covers**: API requests, authentication, testing scripts
   - **Best for**: Developers testing the backend
   - **Length**: Technical (includes code examples)

### 4. **demo_commands.py** 🎮
   - **Purpose**: Interactive demonstration script
   - **Covers**: All commands in executable form
   - **Best for**: Hands-on learning and testing
   - **Usage**: `python demo_commands.py`

---

## 🚀 Quick Start

### For End Users (Natural Language)

**Just chat naturally with TodoBot!**

```
You: "Add buy groceries"
Bot: ✓ Task created: Buy groceries

You: "Show my tasks"
Bot: Your tasks:
     ◯ Buy groceries

You: "Mark it as done"
Bot: ✓ Task completed: Buy groceries
```

### For Developers (API Testing)

```bash
# Get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}' \
  | jq -r '.access_token')

# Send chat message
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Add buy milk"}'
```

---

## 📋 Command Categories

### ➕ Adding Tasks
```
"Add [task]"
"Create a task: [task]"
"Remind me to [task]"
```

### 📋 Listing Tasks
```
"Show my tasks"
"List [all/pending/completed] tasks"
```

### ✏️ Updating Tasks
```
"Update [task] to [new content]"
"Change [task] description to [details]"
```

### ✅ Completing Tasks
```
"Mark [task] as done"
"I finished [task]"
```

### ❌ Deleting Tasks
```
"Delete [task]"
"Remove [task]"
```

---

## 💡 Key Features

### 🗣️ Natural Language Understanding
TodoBot understands various phrasings:
- "Add buy milk" = "Create a task to buy milk" = "Remind me to buy milk"
- All work the same way!

### 🔍 Fuzzy Task Matching
Reference tasks by any distinctive part:
- Task: "Buy groceries from Whole Foods"
- Matches: "groceries", "Whole Foods", "buy groceries"

### 💬 Conversation Context
TodoBot remembers your conversation:
```
You: "Add buy milk"
Bot: ✓ Created

You: "And also add call plumber"
Bot: ✓ Created

You: "Show what I just added"
Bot: ◯ Buy milk
     ◯ Call plumber
```

### 🎯 Smart Disambiguation
When multiple tasks match:
```
Tasks: "Finish report", "Review report", "Submit report"

You: "Complete the report"
Bot: Which one?
     1. Finish report
     2. Review report
     3. Submit report
```

---

## 🎓 Learning Path

### Level 1: Basics (5 minutes)
1. Read **QUICK_REFERENCE.md**
2. Try basic commands:
   - Add a task
   - List tasks
   - Mark as done
   - Delete task

### Level 2: Complete Features (15 minutes)
1. Read **TODOBOT_COMMAND_GUIDE.md** sections 1-5
2. Try all operations
3. Experiment with different phrasings

### Level 3: Advanced Usage (30 minutes)
1. Read complete **TODOBOT_COMMAND_GUIDE.md**
2. Run **demo_commands.py** interactive mode
3. Try multi-task operations
4. Practice task disambiguation

### Level 4: API Testing (Developers)
1. Read **API_TESTING_GUIDE.md**
2. Test with curl commands
3. Set up Postman collection
4. Run automated test script

---

## 🧪 Testing & Verification

### Option 1: Python Script (Recommended)
```bash
cd backend
./venv/Scripts/python.exe demo_commands.py

# Choose:
# 1 = Watch demonstration
# 2 = Interactive mode
```

### Option 2: Direct Agent Test
```bash
./venv/Scripts/python.exe test_agent.py
```

### Option 3: API with curl
```bash
# Follow steps in API_TESTING_GUIDE.md
```

### Option 4: Frontend Chat Interface
1. Start backend: `uvicorn app.main:app --reload`
2. Start frontend: `npm run dev`
3. Navigate to `/chat`
4. Chat naturally with TodoBot

---

## 📝 Common Use Cases

### Daily Task Management
```
Morning:  "Show pending tasks"
During:   "Mark [task] as done" (as completed)
Add new:  "Add [new task]"
Evening:  "Show what I accomplished"
Cleanup:  "Delete completed tasks"
```

### Project Management
```
Setup:    "Add finish proposal, Add review budget, Add schedule meeting"
Progress: "Show pending tasks"
Update:   "Change proposal deadline to Friday"
Complete: "Mark budget review as done"
Review:   "Show completed tasks"
```

### Weekly Planning
```
Plan:     "Add [all tasks for week]"
Daily:    "Show pending tasks"
Review:   "Update [task] with new details"
Complete: "Mark [finished tasks] as done"
Reflect:  "Show completed tasks"
```

---

## 🔧 Troubleshooting

### Command Not Working?

1. **Check phrasing**: Try different variations
   ```
   Instead of: "Set task done"
   Try: "Mark task as done"
   ```

2. **List tasks first**: See exact titles
   ```
   "Show my tasks"
   Then use exact title from the list
   ```

3. **Be specific**: Use distinctive keywords
   ```
   Instead of: "Update the task"
   Try: "Update the groceries task"
   ```

### Task Not Found?

1. **List all tasks**: `"Show my tasks"`
2. **Check spelling**: Use exact words from task title
3. **Use keywords**: Distinctive parts of title

### Multiple Matches?

TodoBot will ask for clarification:
```
Bot: "Which task did you mean?"
You: "The first one" OR "The buy groceries task"
```

---

## 🎯 Best Practices

1. **Use descriptive titles**: Easy to reference later
   - ✅ "Buy groceries from Whole Foods"
   - ❌ "Shopping"

2. **Add descriptions**: Capture important details
   - "Add prepare report with description: include Q4 data and executive summary"

3. **Regular cleanup**: Delete old completed tasks
   - "Delete completed tasks"

4. **Check progress**: Review regularly
   - "Show pending tasks"
   - "Show completed tasks"

5. **Natural conversation**: Don't overthink syntax
   - TodoBot understands natural language!

---

## 📞 Support & Resources

### Documentation
- **Full Guide**: TODOBOT_COMMAND_GUIDE.md
- **Quick Ref**: QUICK_REFERENCE.md
- **API Guide**: API_TESTING_GUIDE.md

### Testing
- **Demo Script**: `python demo_commands.py`
- **Test Agent**: `python test_agent.py`
- **Bash Script**: In API_TESTING_GUIDE.md

### Implementation Details
- **Refactoring**: REFACTORING_SUMMARY.md
- **Status**: IMPLEMENTATION_STATUS.md

---

## 🎨 Example Workflow

### Complete Task Management Session

```
# Start of day
"Show pending tasks"

# Add new tasks
"Add finish quarterly report"
"Add review team budget"
"Add schedule client meeting"

# Check what's pending
"Show my tasks"

# Work on tasks...
# ...

# Update progress
"Update the report task: add deadline Friday 5pm"

# Complete tasks as done
"I finished the budget review"
"Mark the meeting task as done"

# End of day review
"Show what I completed today"
"Show pending tasks"

# Cleanup
"Delete old completed tasks"
```

---

## 🚀 Next Steps

1. **Choose your starting point**:
   - New user? → Start with **QUICK_REFERENCE.md**
   - Want details? → Read **TODOBOT_COMMAND_GUIDE.md**
   - Developer? → Check **API_TESTING_GUIDE.md**
   - Hands-on learner? → Run **demo_commands.py**

2. **Practice**: Try all command types

3. **Explore**: Experiment with different phrasings

4. **Integrate**: Use in your daily workflow

5. **Provide Feedback**: Help improve TodoBot!

---

**Remember**: TodoBot is designed for natural conversation. Just chat normally, and it will understand! 💬✨

---

**Documentation Version**: 1.0
**Last Updated**: 2026-01-24
**Backend Status**: ✅ Fully Operational with OpenAI Agents SDK
