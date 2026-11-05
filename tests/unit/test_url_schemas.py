from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from app.schemas.url import CreateURLRequest, CreateURLResponse


def test_create_url_request_accepts_http_url():
    request = CreateURLRequest(original_url="http://example.com")

    assert str(request.original_url) == "http://example.com/"


def test_create_url_request_accepts_https_url():
    request = CreateURLRequest(original_url="https://example.com/path")

    assert str(request.original_url) == "https://example.com/path"


@pytest.mark.parametrize(
    "url",
    [
        "ftp://example.com",
        "example.com",
        "not-a-url",
        "",
    ],
)
def test_create_url_request_rejects_invalid_urls(url):
    with pytest.raises(ValidationError):
        CreateURLRequest(original_url=url)


# Tests url response schemas
def test_create_url_response_contains_expected_fields():
    response = CreateURLResponse(
        original_url="https://example.com/path",
        short_code="aB3xY9",
        short_url="http://localhost:8000/aB3xY9",
    )

    assert str(response.original_url) == "https://example.com/path"
    assert response.short_code == "aB3xY9"
    assert response.short_url == "http://localhost:8000/aB3xY9"


def test_create_url_request_defaults_expires_at_to_none():
    request = CreateURLRequest(original_url="https://example.com")

    assert request.expires_at is None


def test_create_url_request_accepts_timezone_aware_expiration():
    expires_at = datetime.now(UTC) + timedelta(days=7)

    request = CreateURLRequest(
        original_url="https://example.com",
        expires_at=expires_at,
    )

    assert request.expires_at == expires_at


def test_create_url_request_rejects_timezone_naive_expiration():
    expires_at = datetime(2027, 1, 1)  # noqa: DTZ001

    with pytest.raises(ValidationError):
        CreateURLRequest(
            original_url="https://example.com",
            expires_at=expires_at,
        )
