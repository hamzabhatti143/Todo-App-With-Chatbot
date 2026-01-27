"""
Interactive TodoBot Command Demo

This script demonstrates all available commands with the TodoBot agent.
Run this to see how to add, edit, delete, and manage tasks through natural language.

Usage:
    python demo_commands.py
"""

import asyncio
import sys
sys.path.insert(0, '/mnt/d/todo-fullstack-web/backend')

from app.agent import TodoBot, AgentRequest


async def run_command(agent: TodoBot, user_id: str, command: str, description: str = ""):
    """Execute a command and display the result."""
    print("\n" + "="*70)
    if description:
        print(f"📌 {description}")
    print(f"💬 You: {command}")
    print("-"*70)

    try:
        request = AgentRequest(user_id=user_id, message=command)
        response = await agent.run(request)

        print(f"🤖 TodoBot: {response.message}")

        if response.error:
            print(f"❌ Error: {response.error}")

    except Exception as e:
        print(f"❌ Exception: {e}")


async def demo_all_commands():
    """Demonstrate all TodoBot commands."""

    print("\n" + "🎯"*35)
    print("       TODOBOT COMMAND DEMONSTRATION")
    print("🎯"*35 + "\n")

    # Initialize agent
    print("Initializing TodoBot agent...")
    agent = TodoBot()
    test_user_id = "550e8400-e29b-41d4-a716-446655440000"
    print("✓ Agent ready!\n")

    # ========================================================================
    # SECTION 1: ADDING TASKS
    # ========================================================================

    print("\n" + "📝"*35)
    print("       SECTION 1: ADDING TASKS")
    print("📝"*35)

    await run_command(
        agent, test_user_id,
        "Add a task to buy groceries",
        "Basic task creation"
    )

    await run_command(
        agent, test_user_id,
        "Create a task: finish quarterly report",
        "Alternative phrasing for adding"
    )

    await run_command(
        agent, test_user_id,
        "Remind me to call dentist",
        "Yet another way to add tasks"
    )

    await run_command(
        agent, test_user_id,
        "Add prepare presentation with description: include Q4 sales charts and budget analysis",
        "Adding a task with description"
    )

    # ========================================================================
    # SECTION 2: LISTING TASKS
    # ========================================================================

    print("\n" + "📋"*35)
    print("       SECTION 2: LISTING TASKS")
    print("📋"*35)

    await run_command(
        agent, test_user_id,
        "Show my tasks",
        "List all tasks"
    )

    await run_command(
        agent, test_user_id,
        "What's on my todo list?",
        "Alternative phrasing for listing"
    )

    await run_command(
        agent, test_user_id,
        "Show pending tasks",
        "Filter by pending status"
    )

    # ========================================================================
    # SECTION 3: UPDATING TASKS
    # ========================================================================

    print("\n" + "✏️"*35)
    print("       SECTION 3: UPDATING TASKS")
    print("✏️"*35)

    await run_command(
        agent, test_user_id,
        "Update the groceries task to 'Buy groceries from Whole Foods'",
        "Update task title"
    )

    await run_command(
        agent, test_user_id,
        "Change the report task description to: include executive summary and appendices",
        "Update task description"
    )

    # ========================================================================
    # SECTION 4: COMPLETING TASKS
    # ========================================================================

    print("\n" + "✅"*35)
    print("       SECTION 4: COMPLETING TASKS")
    print("✅"*35)

    await run_command(
        agent, test_user_id,
        "Mark the dentist task as done",
        "Complete a task by title"
    )

    await run_command(
        agent, test_user_id,
        "I finished the groceries task",
        "Alternative phrasing for completion"
    )

    await run_command(
        agent, test_user_id,
        "Show completed tasks",
        "View what's been completed"
    )

    # ========================================================================
    # SECTION 5: DELETING TASKS
    # ========================================================================

    print("\n" + "❌"*35)
    print("       SECTION 5: DELETING TASKS")
    print("❌"*35)

    await run_command(
        agent, test_user_id,
        "Delete the presentation task",
        "Delete a specific task"
    )

    await run_command(
        agent, test_user_id,
        "Remove the report task",
        "Alternative phrasing for deletion"
    )

    # ========================================================================
    # SECTION 6: FINAL STATUS
    # ========================================================================

    print("\n" + "📊"*35)
    print("       SECTION 6: FINAL STATUS")
    print("📊"*35)

    await run_command(
        agent, test_user_id,
        "Show my tasks",
        "Check remaining tasks"
    )

    await run_command(
        agent, test_user_id,
        "What have I completed?",
        "Review completed tasks"
    )

    # ========================================================================
    # SUMMARY
    # ========================================================================

    print("\n" + "🎓"*35)
    print("       DEMONSTRATION COMPLETE")
    print("🎓"*35 + "\n")

    print("Key Takeaways:")
    print("1. ✅ TodoBot understands natural language - no rigid syntax needed")
    print("2. ✅ Multiple phrasings work for the same action")
    print("3. ✅ Tasks are referenced by title (fuzzy matching)")
    print("4. ✅ You can add descriptions for more detail")
    print("5. ✅ All operations are conversational and user-friendly")

    print("\n" + "="*70)
    print("Try these commands yourself in the chat interface!")
    print("="*70 + "\n")


async def interactive_mode():
    """Interactive mode - chat with TodoBot."""

    print("\n" + "💬"*35)
    print("       INTERACTIVE MODE")
    print("💬"*35 + "\n")

    agent = TodoBot()
    test_user_id = "550e8400-e29b-41d4-a716-446655440000"

    print("Type your commands below (or 'quit' to exit):\n")

    while True:
        try:
            command = input("You: ").strip()

            if command.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋\n")
                break

            if not command:
                continue

            request = AgentRequest(user_id=test_user_id, message=command)
            response = await agent.run(request)

            print(f"\nTodoBot: {response.message}\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋\n")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


async def main():
    """Main entry point."""

    print("\nTodoBot Command Demo")
    print("=" * 70)
    print("\nChoose mode:")
    print("1. Run demonstration of all commands")
    print("2. Interactive mode (chat with TodoBot)")
    print()

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        await demo_all_commands()
    elif choice == "2":
        await interactive_mode()
    else:
        print("Invalid choice. Running demonstration...")
        await demo_all_commands()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExiting...\n")
