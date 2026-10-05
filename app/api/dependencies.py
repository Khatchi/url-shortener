from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.repositories.url import URLRepository
from app.services.url import URLService


def get_url_service(request: Request) -> URLService:
    session_factory: async_sessionmaker[AsyncSession] = request.app.state.session_factory

    repository = URLRepository(session_factory)

    return URLService(repository)

