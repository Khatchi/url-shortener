from unittest.mock import AsyncMock, Mock
from sqlalchemy.exc import IntegrityError

import pytest

from app.models.url import URL
from app.services.url import URLService


@pytest.mark.asyncio
async def test_create_url_generates_short_code_and_persists_url():
    repository = Mock()
    repository.create = AsyncMock(
        side_effect=lambda url: url,
    )

    service = URLService(repository)

    result = await service.create_url("https://example.com/path")

    assert isinstance(result, URL)
    assert result.original_url == "https://example.com/path"
    assert len(result.short_code) == 6
    assert repository.create.await_count == 1

    persisted_url = repository.create.await_args.args[0]

    assert persisted_url.original_url == "https://example.com/path"
    assert len(persisted_url.short_code) == 6


@pytest.mark.asyncio
async def test_create_url_retries_when_short_code_collides(monkeypatch):
    repository = Mock()

    first_error = IntegrityError(
        statement="INSERT INTO urls",
        params={},
        orig=Mock(
            pgcode="23505",
            args=("duplicate key value violates unique constraint",),
        ),
    )

    existing_url = URL(
        original_url="https://example.com/first",
        short_code="abc123",
    )

    repository.create = AsyncMock(
        side_effect=[
            first_error,
            existing_url,
        ]
    )

    generated_codes = iter(["abc123", "xyz789"])
    monkeypatch.setattr(
        "app.services.url.generate_short_code",
        lambda: next(generated_codes),
    )

    service = URLService(repository)

    result = await service.create_url("https://example.com/second")

    assert result is existing_url
    assert repository.create.await_count == 2

    first_attempt = repository.create.await_args_list[0].args[0]
    second_attempt = repository.create.await_args_list[1].args[0]

    assert first_attempt.short_code == "abc123"
    assert second_attempt.short_code == "xyz789"



@pytest.mark.asyncio
async def test_create_url_fails_after_max_retries(monkeypatch):
    repository = Mock()

    duplicate_error = IntegrityError(
        statement="INSERT INTO urls",
        params={},
        orig=Mock(
            pgcode="23505",
            args=("duplicate key value violates unique constraint",),
        ),
    )

    repository.create = AsyncMock(side_effect=duplicate_error)

    monkeypatch.setattr(
        "app.services.url.generate_short_code",
        lambda: "abc123",
    )

    service = URLService(repository)

    with pytest.raises(RuntimeError, match="Failed to generate a unique short code"):
        await service.create_url("https://exiample.com")

    assert repository.create.await_count == 3
