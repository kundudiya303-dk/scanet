"""
scanet — Database Connection & Initialization
SQLite with Write-Ahead Logging (WAL) mode for concurrent reads.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.engine import make_url
from config import settings
from pathlib import Path

database_url = make_url(settings.DATABASE_URL)
if database_url.get_backend_name() == "sqlite":
    database_path = database_url.database
    if database_path and database_path != ":memory:":
        path = Path(database_path)
        if not path.is_absolute():
            path = Path(__file__).resolve().parent.parent / path
        path.parent.mkdir(parents=True, exist_ok=True)
        database_url = database_url.set(database=str(path))

engine = create_async_engine(
    database_url,
    echo=settings.DEBUG,
    connect_args={
        "check_same_thread": False,
        # Enable WAL mode and foreign key enforcement
    },
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def init_db():
    """Create all tables on startup."""
    async with engine.begin() as conn:
        # Enable WAL mode for better concurrent performance
        await conn.exec_driver_sql("PRAGMA journal_mode=WAL")
        await conn.exec_driver_sql("PRAGMA foreign_keys=ON")
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    """Dependency — yields an async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
