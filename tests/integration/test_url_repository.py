import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models.url import URL
from app.repositories.url import URLRepository


@pytest.mark.asyncio
async def test_create_url_persists_url(session_factory: async_sessionmaker[AsyncSession]):
    repository = URLRepository(session_factory)

    url = URL(
        id=uuid.uuid4(),
        original_url="https://example.com",
        short_code="aB3xY9",
    )

    created = await repository.create(url)

    assert created.id == url.id
    assert created.original_url == "https://example.com"
    assert created.short_code == "aB3xY9"
    assert created.created_at is not None


@pytest.mark.asyncio
async def test_get_by_short_code_returns_url(session_factory: async_sessionmaker[AsyncSession]):
    repository = URLRepository(session_factory)

    url = URL(
        id=uuid.uuid4(),
        original_url="https://example.com/path",
        short_code="xY7kP2",
    )

    await repository.create(url)

    found = await repository.get_by_short_code("xY7kP2")

    assert found is not None
    assert found.id == url.id
    assert found.original_url == "https://example.com/path"


@pytest.mark.asyncio
async def test_get_by_short_code_returns_none_when_not_found(
        session_factory: async_sessionmaker[AsyncSession]):

    repository = URLRepository(session_factory)

    found = await repository.get_by_short_code("missing")

    assert found is None

