import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.db.base import Base
from app.db.session import create_engine
from app.main import create_app


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_url_with_real_application():
    settings = Settings()

    if settings.test_database_url is None:
        pytest.fail("TEST_DATABASE_URL is not configured")

    test_settings = Settings(
        database_url=settings.test_database_url,
        base_url="http://localhost:8000",
    )

    engine = create_engine(test_settings)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    try:
        app = create_app(test_settings)

        with TestClient(app) as client:
            response = client.post(
                "/api/v1/urls",
                json={"original_url": "https://example.com/path"},
            )

        assert response.status_code == 201

        data = response.json()

        assert data["original_url"] == "https://example.com/path"
        assert len(data["short_code"]) == 6
        assert data["short_url"] == (
            f"http://localhost:8000/{data['short_code']}"
        )
    finally:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)

        await engine.dispose()
