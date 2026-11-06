from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError

from app.core.short_code import generate_short_code
from app.models.url import URL
from app.repositories.url import URLRepository

_MAX_CREATE_ATTEMPTS = 3


class URLService:
    def __init__(self, repository: URLRepository):
        self._repository = repository

    async def create_url(
        self, original_url: str, expires_at: datetime | None = None
    ) -> URL:

        for _ in range(_MAX_CREATE_ATTEMPTS):
            url = URL(
                original_url=original_url,
                short_code=generate_short_code(),
                expires_at=expires_at,
            )

            if expires_at is not None and expires_at <= datetime.now(UTC):
                raise ValueError("Expiration date must be in the future")

            try:
                return await self._repository.create(url)
            except IntegrityError as exc:
                if getattr(exc.orig, "pgcode", None) != "23505":
                    raise

        raise RuntimeError("Failed to generate a unique short code")

    async def get_url(self, short_code: str) -> URL | None:
        url = await self._repository.get_by_short_code(short_code)

        if url is None:
            return None

        if url.expires_at is not None and url.expires_at <= datetime.now(UTC):
            return None

        return url
