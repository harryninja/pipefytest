from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers.clients import router as clients_router
from app.api.routers.health import router as health_router
from app.api.routers.webhooks import router as webhooks_router
from app.core.database import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Mundo Invest Client Management API",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.include_router(health_router)
    app.include_router(clients_router)
    app.include_router(webhooks_router)
    return app


app = create_app()
