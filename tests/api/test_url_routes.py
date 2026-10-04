from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.urls import get_url_service, router, get_settings
from app.models.url import URL
from app.core.config import Settings


def create_test_app(service: Mock) -> FastAPI:
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")

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
