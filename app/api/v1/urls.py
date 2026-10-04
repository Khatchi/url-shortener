from fastapi import APIRouter, Depends

from app.core import short_code
from app.core.config import Settings
from app.schemas.url import CreateURLRequest, CreateURLResponse
from app.services.url import URLService

router = APIRouter()

def get_url_service() -> URLService:
    raise NotImplementedError


def get_settings() -> Settings:
    return Settings()


@router.post("/urls",response_model=CreateURLResponse, status_code=201)
async def create_url(request: CreateURLRequest, 
                     service: URLService = Depends(get_url_service),
                     settings: Settings = Depends(get_settings),
                    ) -> CreateURLResponse:

    url = await service.create_url(str(request.original_url))

    return CreateURLResponse(
        original_url=url.original_url,
        short_code=url.short_code,
        short_url=f"{settings.base_url.rstrip('/')}/{url.short_code}",
    )

