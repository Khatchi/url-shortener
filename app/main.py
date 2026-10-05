from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.urls import redirect_router, router
from app.core.config import Settings
from app.db.session import create_engine, create_session_factory


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        engine = create_engine(settings)
        session_factory = create_session_factory(engine)

        app.state.session_factory = session_factory

        yield

        await engine.dispose()

    app = FastAPI(lifespan=lifespan)

    app.include_router(router, prefix="/api/v1")
    app.include_router(redirect_router)

    return app
