# TodoBot Command Guide

**Natural Language Interface for Task Management**

TodoBot understands natural language commands. You don't need to use specific syntax - just chat naturally!

---

## 📝 Adding Tasks

### Basic Task Creation

**Examples:**
```
"Add a task to buy groceries"
"Create a task: finish the report"
"Remind me to call mom"
"I need to schedule a dentist appointment"
"Add buy milk to my todo list"
```

**Response:**
```
✓ Task created: Buy groceries
```

### Task with Description

**Examples:**
```
"Add a task to buy groceries with description: milk, eggs, bread"
"Create a task: finish report, details: quarterly sales analysis due Friday"
"Add prepare presentation and include talking points about Q4 results"
```

**Response:**
```
✓ Task created: Buy groceries
  Description: milk, eggs, bread
```

---

## 📋 Viewing Tasks

### List All Tasks

**Examples:**
```
"Show my tasks"
"What's on my todo list?"
"List all my tasks"
"Show me what I need to do"
"What tasks do I have?"
```

**Response:**
```
Your tasks:
◯ Buy groceries
◯ Finish the report
✓ Call mom (completed)
```

### Filter by Status

**Pending Tasks Only:**
```
"Show my pending tasks"
"What tasks are not done?"
"List incomplete tasks"
"Show what I still need to do"
```

**Completed Tasks Only:**
```
"Show completed tasks"
"What have I finished?"
"List done tasks"
"Show my accomplishments"
```

---

## ✏️ Editing/Updating Tasks

### Update Task Title

**Examples:**
```
"Change the groceries task to 'Buy groceries and fruits'"
"Update the report task title to 'Finish quarterly report'"
"Rename the dentist task to 'Dentist appointment at 2pm'"
```

**How it works:**
1. TodoBot will first list your tasks to find the one you're referring to
2. Match the task by title (fuzzy matching)
3. Update the title

**Response:**
```
Let me find that task for you...

✓ Task updated: Buy groceries → Buy groceries and fruits
```

### Update Task Description

**Examples:**
```
"Update the groceries task description to: milk, eggs, bread, cheese"
"Change the report task details to include Q4 analysis"
"Add to the presentation task: include sales charts"
```

**Response:**
```
✓ Task updated
  New description: milk, eggs, bread, cheese
```

### Update Both Title and Description

**Examples:**
```
"Update the groceries task: change title to 'Weekly shopping' and add description 'Whole Foods, get organic produce'"
```

---

## ✅ Marking Tasks Complete

### Complete a Task

**Examples:**
```
"Mark the groceries task as done"
"Complete the report task"
"I finished the presentation"
"The dentist task is done"
"Check off buy milk"
```

**How it works:**
1. TodoBot lists your tasks to find the match
2. Identifies the task by title
3. Marks it as completed

**Response:**
```
✓ Task completed: Buy groceries
  Great job! ✓
```

### Complete Multiple Tasks

**Examples:**
```
"Mark groceries and report as done"
"Complete the presentation and meeting tasks"
```

---

## ❌ Deleting Tasks

### Delete a Task

**Examples:**
```
"Delete the groceries task"
"Remove the report task"
"Cancel the dentist appointment task"
"Get rid of the old presentation task"
```

**How it works:**
1. TodoBot lists your tasks to find the match
2. Identifies the task by title
3. Permanently removes it

**Response:**
```
Let me find that task...

✓ Task deleted: Buy groceries
```

### Delete All Completed Tasks

**Examples:**
```
"Delete all completed tasks"
"Clear finished tasks"
"Remove all done items"
```

---

## 🔍 Task Identification

### How TodoBot Finds Your Tasks

When you reference a task by name (not ID), TodoBot:

1. **Lists your tasks** - Retrieves all your tasks
2. **Fuzzy matches** - Finds tasks with similar titles (case-insensitive)
3. **Single match** - If one task matches, uses it automatically
4. **Multiple matches** - Asks you to clarify which one
5. **No match** - Tells you the task wasn't found

### Examples of Fuzzy Matching

**Your task:** "Buy groceries from Whole Foods"

**These will match:**
- "Complete the groceries task"
- "Update the Whole Foods task"
- "Delete buy groceries"
- "Mark groceries as done"

### When Multiple Tasks Match

**Scenario:** You have:
- "Finish report"
- "Review report"
- "Submit report"

**Command:** "Complete the report task"

**TodoBot Response:**
```
I found multiple tasks with "report":
1. Finish report
2. Review report
3. Submit report

Which one did you mean? (reply with the number or full title)
```

---

## 💡 Advanced Commands

### Multi-part Requests

**Examples:**
```
"Add buy milk and also add call plumber"
```

TodoBot will:
- Create first task: "Buy milk"
- Create second task: "Call plumber"

### Contextual Follow-ups

```
User: "Show my tasks"
Bot: [Lists tasks including "Buy groceries"]

User: "Mark the first one as done"
Bot: ✓ Task completed: Buy groceries
```

### Natural Variations

TodoBot understands many phrasings:

**For Adding:**
- "Add...", "Create...", "Make a task...", "Remind me to...", "I need to..."

**For Listing:**
- "Show...", "List...", "What...", "Display...", "Get..."

**For Completing:**
- "Complete...", "Mark as done...", "Finish...", "Done with...", "Check off..."

**For Deleting:**
- "Delete...", "Remove...", "Cancel...", "Get rid of..."

**For Updating:**
- "Update...", "Change...", "Modify...", "Edit...", "Rename..."

---

## 🎯 Complete Workflow Example

### Scenario: Managing a Work Project

```
User: "Add a task: finish project proposal"
Bot: ✓ Task created: Finish project proposal

User: "Add review budget spreadsheet"
Bot: ✓ Task created: Review budget spreadsheet

User: "Show my tasks"
Bot: Your tasks:
     ◯ Finish project proposal
     ◯ Review budget spreadsheet

User: "Update the proposal task to include deadline: Friday 5pm"
Bot: ✓ Task updated
     Description: deadline: Friday 5pm

User: "I finished the budget review"
Bot: ✓ Task completed: Review budget spreadsheet
     Great work! ✓

User: "Show pending tasks"
Bot: Your pending tasks:
     ◯ Finish project proposal (deadline: Friday 5pm)

User: "Mark the proposal as done"
Bot: ✓ Task completed: Finish project proposal
     Excellent! All caught up! ✓

User: "Show completed tasks"
Bot: Your completed tasks:
     ✓ Review budget spreadsheet
     ✓ Finish project proposal
```

---

## ⚙️ Testing Commands (Development)

### Using the Test Script

Run the agent test script:

```bash
cd backend
./venv/Scripts/python.exe test_agent.py
```

### Using the Chat API

**Endpoint:** `POST /api/chat`

**Request:**
```json
{
  "content": "Add a task to buy groceries",
  "conversation_id": null
}
```

**Response:**
```json
{
  "conversation_id": "uuid-here",
  "message_id": "uuid-here",
  "role": "assistant",
  "content": "I've created the task to buy groceries. If you need anything else, just let me know!",
  "created_at": "2026-01-24T12:00:00Z",
  "task_data": {}
}
```

### Using curl

```bash
# Add a task
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "content": "Add a task to buy groceries"
  }'

# List tasks
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "content": "Show my tasks",
    "conversation_id": "previous-conversation-id"
  }'

# Update a task
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "content": "Update the groceries task to include milk and bread"
  }'

# Complete a task
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "content": "Mark the groceries task as done"
  }'

# Delete a task
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "content": "Delete the groceries task"
  }'
```

---

## 🚀 Quick Reference

| Action | Example Command |
|--------|----------------|
| **Add** | "Add a task to buy groceries" |
| **List All** | "Show my tasks" |
| **List Pending** | "Show pending tasks" |
| **List Completed** | "Show completed tasks" |
| **Update Title** | "Change groceries task to 'Weekly shopping'" |
| **Update Description** | "Update groceries task description to: milk, eggs, bread" |
| **Complete** | "Mark groceries task as done" |
| **Delete** | "Delete the groceries task" |

---

## 💬 Tips for Best Results

1. **Be Specific**: Use descriptive task titles
   - ✅ "Buy groceries from Whole Foods"
   - ❌ "Shopping"

2. **Use Keywords**: Include action words for clarity
   - "Add", "Update", "Delete", "Complete"

3. **Reference Tasks Clearly**: Use unique parts of the task title
   - ✅ "Complete the Whole Foods task"
   - ❌ "Complete that task"

4. **Ask for Help**: TodoBot will ask for clarification if needed
   - It's okay to be conversational!

5. **Check Your Tasks**: List tasks regularly to see what needs to be done

---

## 🔧 Troubleshooting

### "I can't find that task"

**Cause:** Task title doesn't match
**Solution:**
```
"Show my tasks"  # First, see what tasks you have
"Delete the exact title from the list"
```

### Multiple matches

**Cause:** Similar task titles
**Solution:** Use more specific parts of the title
```
Instead of: "Complete the report"
Try: "Complete the quarterly sales report"
```

### Task not updating

**Cause:** Ambiguous reference
**Solution:**
```
# First list tasks to see exact titles
"Show my tasks"

# Then use exact title
"Update 'Buy groceries' to 'Weekly grocery shopping'"
```

---

## 📱 Frontend Usage (React App)

### Chat Interface

Users interact through the `/chat` page:

1. **Type message** in the input box
2. **Send** the message
3. **Receive response** from TodoBot
4. **Continue conversation** naturally

### Example Session

```
You: Add buy milk
Bot: ✓ Task created: Buy milk

You: And also add call dentist
Bot: ✓ Task created: Call dentist

You: What do I need to do?
Bot: Your tasks:
     ◯ Buy milk
     ◯ Call dentist

You: Done with the milk
Bot: ✓ Task completed: Buy milk
```

---

## 🎓 Learning the System

### Start Simple

1. Add a task: `"Add a task to test"`
2. View it: `"Show my tasks"`
3. Complete it: `"Mark test as done"`
4. Delete it: `"Delete the test task"`

### Practice Variations

Try different phrasings for the same action:
- "Add buy milk"
- "Create a task to buy milk"
- "Remind me to buy milk"
- "I need to buy milk"

All will work!

---

## 📞 Support

If TodoBot doesn't understand your command:

1. **Try rephrasing**: Use simpler language
2. **Be explicit**: Use keywords like "add", "delete", "update"
3. **List first**: See your tasks, then reference by exact title
4. **Check logs**: Developers can check backend logs for issues

---

**Remember**: TodoBot is conversational AI - talk to it naturally, and it will understand! 🤖✨
