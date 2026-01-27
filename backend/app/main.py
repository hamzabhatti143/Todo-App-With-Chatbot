"""
FastAPI Todo Application

Main application entry point for the FastAPI backend.
Configures CORS, middleware, and routes.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.database import create_db_and_tables
from app.mcp_server.tool_registry import tool_registry
# Note: MCP tools are registered automatically by FastMCP decorator
# from app.mcp_server.tools import mcp  # Uncomment if manual registration needed
from app.middleware.logging import LoggingMiddleware

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Todo API",
    description="RESTful API for todo task management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware for request/response tracking
app.add_middleware(LoggingMiddleware)


@app.on_event("startup")
async def on_startup():
    """Initialize database and register MCP tools on startup"""
    # Initialize database
    create_db_and_tables()

    # Note: MCP tools are registered automatically by @mcp.tool() decorator in tools.py
    # Manual registration not needed with FastMCP
    print("MCP Tool Registry initialized")


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint for health check"""
    return {
        "status": "healthy",
        "message": "Todo API is running",
        "version": "1.0.0"
    }

@app.get("/test-logging")
async def test_logging():
    """Test endpoint to verify logging is working"""
    import logging
    logger = logging.getLogger(__name__)
    logger.info("TEST LOGGING - This message should appear in logs")
    logger.error("TEST ERROR - This error should appear in logs")
    return {"status": "logged", "message": "Check server logs for test messages"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint with database connectivity verification.

    Returns:
        200 OK if healthy with database connected
        503 Service Unavailable if database is unreachable
    """
    from sqlmodel import Session, select, text
    from app.database import engine

    try:
        # Try to execute a simple query to verify database connectivity
        with Session(engine) as session:
            session.exec(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        # Database is unreachable
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "error": "Database connection failed"
            }
        )

# Import and include routers
from app.routes import auth_router, tasks_router, chat_router, conversations_router

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks_router, prefix="/api", tags=["tasks"])
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(conversations_router, prefix="/api", tags=["conversations"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
