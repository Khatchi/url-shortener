from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models.url import URL


class URLRepository:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory


    async def create(self, url: URL) -> URL:
        async with self._session_factory() as session:
            session.add(url)
            await session.commit()
            await session.refresh(url)
            return url

    
    async def get_by_short_code(self, short_code: str) -> URL | None:
        async with self._session_factory() as session:
            result = await session.execute(
                select(URL).where(URL.short_code == short_code)
            )

            return result.scalar_one_or_none()

