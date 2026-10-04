from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.urls import (
    get_url_service,
    router,
    get_settings,
    redirect_router,
)
from app.models.url import URL
from app.core.config import Settings


def create_test_app(service: Mock) -> FastAPI:
    app = FastAPI()

    app.include_router(router, prefix="/api/v1")
    app.include_router(redirect_router)

    settings = Settings(
        database_url="postgresql+asyncpg://test",
        base_url="https://short.example.com",
    )

    app.dependency_overrides[get_url_service] = lambda: service
    app.dependency_overrides[get_settings] = lambda: settings

    return app


def test_create_url_returns_created_url():
    service = Mock()

    created_url = URL(
        id=uuid4(),
        original_url="https://example.com/path",
        short_code="aB3xY9",
    )

    service.create_url = AsyncMock(return_value=created_url)

    app = create_test_app(service)
    client = TestClient(app)

    response = client.post(
        "/api/v1/urls",
        json={"original_url": "https://example.com/path"},
    )

    assert response.status_code == 201

    assert response.json() == {
        "original_url": "https://example.com/path",
        "short_code": "aB3xY9",
        "short_url": "https://short.example.com/aB3xY9",
    }

    service.create_url.assert_awaited_once_with(
        "https://example.com/path",
    )


# tests GET get_url
def test_redirects_to_original_url():
    service = Mock()

    url = URL(
        id=uuid4(),
        original_url="https://example.com/path",
        short_code="aB3xY9",
    )

    service.get_url = AsyncMock(return_value=url)

    app = create_test_app(service)
    client = TestClient(app)

    response = client.get(
        "/aB3xY9",
        follow_redirects=False,
    )

    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com/path"

    service.get_url.assert_awaited_once_with("aB3xY9")


def test_redirect_returns_404_when_short_code_not_found():
    service = Mock()

    service.get_url = AsyncMock(return_value=None)

    app = create_test_app(service)
    client = TestClient(app)

    response = client.get(
        "/missing",
        follow_redirects=False,
    )

    assert response.status_code == 404

    service.get_url.assert_awaited_once_with("missing")
