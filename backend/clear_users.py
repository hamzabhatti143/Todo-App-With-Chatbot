"""
Clear all users from the database

WARNING: This script will delete ALL users and their associated tasks and conversations!
Use with caution, especially in production.
"""

from sqlmodel import Session, select, delete
from app.database import engine
from app.models.user import User
from app.models.task import Task
from app.models.conversation import Conversation
from app.models.message import Message


def clear_all_users():
    """Delete all users and their associated data from the database."""
    with Session(engine) as session:
        try:
            # Delete all messages first (foreign key to conversations)
            result = session.exec(delete(Message))
            messages_deleted = result.rowcount
            print(f"Deleted {messages_deleted} messages")

            # Delete all conversations
            result = session.exec(delete(Conversation))
            conversations_deleted = result.rowcount
            print(f"Deleted {conversations_deleted} conversations")

            # Delete all tasks
            result = session.exec(delete(Task))
            tasks_deleted = result.rowcount
            print(f"Deleted {tasks_deleted} tasks")

            # Delete all users
            result = session.exec(delete(User))
            users_deleted = result.rowcount
            print(f"Deleted {users_deleted} users")

            # Commit the transaction
            session.commit()

            print("\nAll users and associated data have been deleted successfully!")

        except Exception as e:
            session.rollback()
            print(f"\nError clearing users: {e}")
            raise


if __name__ == "__main__":
    print("WARNING: This will delete ALL users and their data!")
    print("=" * 60)

    confirm = input("Type 'DELETE ALL' to confirm: ")

    if confirm == "DELETE ALL":
        clear_all_users()
    else:
        print("\nDeletion cancelled. No data was deleted.")
