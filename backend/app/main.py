from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import setup_logging
from app.core.redis import close_redis
from app.messaging.rabbitmq import rabbitmq_client


@asynccontextmanager
async def lifespan(_app: FastAPI):
    setup_logging()
    try:
        await rabbitmq_client.connect()
    except Exception:
        pass  # health check will report rabbitmq status
    yield
    await rabbitmq_client.close()
    await close_redis()


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        description="Event-driven order and workflow processing platform",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)
    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
