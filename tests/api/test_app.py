from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app


def test_create_app_starts_successfully():
    settings = Settings(
        database_url="postgresql+asyncpg://test",
        base_url="http://localhost:8000",
    )

    app = create_app(settings)

    with TestClient(app):
        assert app.state.session_factory is not None
