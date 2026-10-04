import pytest
from pydantic import ValidationError

from app.core.config import Settings


# tests load from env
def test_settings_load_from_environment(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/url_shortener",
    )

    monkeypatch.setenv("BASE_URL", "http://localhost:8000")

    settings = Settings()

    assert (
        settings.database_url
        == "postgresql+asyncpg://postgres:postgres@localhost:5432/url_shortener"
    )
    assert settings.base_url == "http://localhost:8000"


# checks db url required
def test_database_url_is_required(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


# tests defaults or db url fallbacks
def test_base_url_defaults_to_localhost(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/url_shortener",
    )
    monkeypatch.delenv("BASE_URL", raising=False)

    settings = Settings()

    assert settings.base_url == "http://localhost:8000"



def test_test_database_url_is_loaded(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+asyncpg://kachim:kachim@localhost:5433/url_shortener",
    )
    monkeypatch.setenv(
        "TEST_DATABASE_URL",
        "postgresql+asyncpg://kachim:kachim@localhost:5433/url_shortener_test",
    )

    settings = Settings()

    assert (
        settings.test_database_url
        == "postgresql+asyncpg://kachim:kachim@localhost:5433/url_shortener_test"
    )

