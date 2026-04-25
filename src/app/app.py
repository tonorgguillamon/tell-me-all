import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from src.app.routers.cards import router as cards_router
from src.app.routers.dashboards import router as dashboards_router
from src.app.routers.events import router as events_router
from src.app.routers.sources import router as sources_router
from src.app.routers.users import router as users_router
from src.app.routers.auth import router as auth_router
from storage.db_engine import engine, init_db

# Ensure models are imported so metadata is populated before create_all runs.
from storage import models

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up — initialising database")
    await init_db()
    logger.info("Database ready")
    try:
        yield
    finally:
        logger.info("Shutting down — disposing engine")
        await engine.dispose()


app = FastAPI(
    title="Tell Me All API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_UI_DIR = Path(__file__).parent.parent.parent / "src" / "ui"
app.mount("/ui", StaticFiles(directory=_UI_DIR, html=True), name="ui")


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = [
        {"field": " -> ".join(str(loc) for loc in err["loc"]), "message": err["msg"]}
        for err in exc.errors()
    ]
    return JSONResponse(status_code=422, content={"detail": errors})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

API_PREFIX = "/api/v1"

app.include_router(users_router, prefix=API_PREFIX)
app.include_router(dashboards_router, prefix=API_PREFIX)
app.include_router(cards_router, prefix=API_PREFIX)
app.include_router(events_router, prefix=API_PREFIX)
app.include_router(sources_router, prefix=API_PREFIX)
app.include_router(auth_router)

# uvicorn src.app.app:app --reload
# http://localhost:8000/ui/index.html