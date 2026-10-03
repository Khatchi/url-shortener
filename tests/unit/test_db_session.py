from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from app.core.config import Settings
from app.db.session import create_engine, create_session_factory


def test_create_engine_returns_async_engine():
    settings = Settings(
        database_url="postgresql+asyncpg://postgres:postgres@localhost:5432/url_shortener"
    )

    engine = create_engine(settings)

    assert isinstance(engine, AsyncEngine)


def test_create_session_factory_uses_engine():
    settings = Settings(
        database_url="postgresql+asyncpg://postgres:postgres@localhost:5432/url_shortener"
    )

    engine = create_engine(settings)
    session_factory = create_session_factory(engine)

    assert isinstance(session_factory, async_sessionmaker)
    assert session_factory.kw["bind"] is engine
    assert session_factory.kw["expire_on_commit"] is False


