import app.core.logger  # noqa: F401 — triggers logging config at startup

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_config
from app.middleware.auth import AuthMiddleware
from app.routers import aggregate, construction, health, markets, opex


def create_app() -> FastAPI:
    config = get_config()

    application = FastAPI(title="Enigma BE", version="0.1.0")

    application.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(AuthMiddleware)

    application.include_router(health.router)
    application.include_router(markets.router)
    application.include_router(opex.router)
    application.include_router(construction.router)
    application.include_router(aggregate.router)

    return application
