from sqlalchemy.exc import IntegrityError

from app.core.short_code import generate_short_code
from app.models.url import URL
from app.repositories.url import URLRepository

_MAX_CREATE_ATTEMPTS = 3


class URLService:
    def __init__(self, repository: URLRepository):
        self._repository = repository


    async def create_url(self, original_url: str) -> URL:
        for _ in range(_MAX_CREATE_ATTEMPTS):
            url = URL(
                original_url=original_url,
                short_code=generate_short_code(),
            )

            try:
                return await self._repository.create(url)
            except IntegrityError as exc:
                if getattr(exc.orig, "pgcode", None) != "23505":
                    raise

        raise RuntimeError("Failed to generate a unique short code")


