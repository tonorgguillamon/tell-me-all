from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.routers.cards import router as cards_router
from src.app.routers.dashboards import router as dashboards_router
from src.app.routers.events import router as events_router
from src.app.routers.sources import router as sources_router
from src.app.routers.users import router as users_router
from storage.db_engine import engine, init_db

# Ensure models are imported so metadata is populated before create_all runs.
from storage import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    try:
        yield
    finally:
        await engine.dispose()


app = FastAPI(
    title="Tell Me All API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(users_router)
app.include_router(dashboards_router)
app.include_router(cards_router)
app.include_router(events_router)
app.include_router(sources_router)