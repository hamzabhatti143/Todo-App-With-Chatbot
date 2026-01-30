"""Application configuration settings."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str

    # Authentication
    better_auth_secret: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: str = "http://localhost:3000"

    # Application
    debug: bool = False

    # OpenAI API Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.3  # Reduced from 0.7 for faster, more focused responses
    openai_max_tokens: int = 512  # Reduced from 1024 for faster generation
    openai_timeout: int = 30

    # Rate Limiting
    rate_limit_chat: str = "20/minute"  # Increased from 10 for smoother experience
    rate_limit_agent: str = "15/minute"  # Increased from 5 for faster interactions

    # Optional: Redis for rate limiting
    redis_url: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
settings = Settings()
