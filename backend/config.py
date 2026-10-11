"""
scanet — Application Configuration
Loads settings from environment variables with sensible defaults.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "change-this-in-production"
    CORS_ORIGINS: List[str] = ["http://localhost:8000", "http://127.0.0.1:8000"]

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/scanet.db"

    # Tool Binaries
    TOOL_BIN_DIR: str = "/opt/scanet/bin"

    # Job Engine
    MAX_CONCURRENT_JOBS: int = 2
    DEFAULT_JOB_TIMEOUT: int = 600  # seconds

    # Wordlists
    WORDLIST_DIR: str = "../wordlists"

    # Scope — block these from being scanned under any circumstances
    BLOCKED_CIDRS: List[str] = [
        "127.0.0.0/8",      # Loopback
        "169.254.0.0/16",   # Link-local / AWS IMDS
        "::1/128",          # IPv6 loopback
        "fc00::/7",         # IPv6 private
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
