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
