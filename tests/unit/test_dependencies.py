from types import SimpleNamespace

from fastapi import Request

from app.api.dependencies import get_url_service
from app.repositories.url import URLRepository
from app.services.url import URLService


def test_get_url_service_builds_service_from_session_factory():
    session_factory = object()

    app = SimpleNamespace(
        state=SimpleNamespace(
            session_factory=session_factory,
        )
    )

    request = Request(
        {
            "type": "http",
            "app": app,
        }
    )

    service = get_url_service(request)

    assert isinstance(service, URLService)
    assert isinstance(service._repository, URLRepository)
    assert service._repository._session_factory is session_factory
