"""
FastAPI Todo Application

Main application entry point for the FastAPI backend.
Configures CORS, middleware, and routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.database import create_db_and_tables

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


@app.on_event("startup")
async def on_startup():
    """Initialize database on startup"""
    create_db_and_tables()


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint for health check"""
    return {
        "status": "healthy",
        "message": "Todo API is running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

# Import and include routers
from app.routes import auth_router, tasks_router

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks_router, prefix="/api", tags=["tasks"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
