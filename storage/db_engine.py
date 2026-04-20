from __future__ import annotations

import os
from typing import AsyncIterator
from urllib.parse import quote_plus

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from dotenv import load_dotenv
load_dotenv()


def _build_database_url() -> str:
    direct_url = os.getenv("DATABASE_URL")
    if direct_url is not None and direct_url.strip() != "":
        return direct_url.strip()

    driver = os.getenv("DB_DRIVER")
    user = os.getenv("POSTGRES_USER")
    raw_password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    database = os.getenv("POSTGRES_DB")

    if not all([
        driver,
        user,
        raw_password,
        host,
        port,
        database,
    ]):
        raise RuntimeError("Missing required database environment variables")

    password = quote_plus(raw_password)
    return f"{driver}://{user}:{password}@{host}:{port}/{database}"


DATABASE_URL = _build_database_url()

class Base(DeclarativeBase):
    pass

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)