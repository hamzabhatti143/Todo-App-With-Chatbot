"""
Database Connection and Session Management
"""

from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/todo_db")

# Create engine with connection pooling (optimized for performance)
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Disable SQL query logging for better performance
    pool_pre_ping=True,  # Verify connections before using
    pool_size=20,  # Increased pool size for better concurrency
    max_overflow=20,  # Increased overflow for peak loads
    pool_recycle=3600,  # Recycle connections after 1 hour
)


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency for database sessions.

    Usage in FastAPI endpoints:
    ```python
    @app.get("/items")
    def read_items(session: Session = Depends(get_session)):
        items = session.exec(select(Item)).all()
        return items
    ```
    """
    with Session(engine) as session:
        yield session
