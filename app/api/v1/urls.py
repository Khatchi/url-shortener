from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from app.api.dependencies import get_url_service
from app.core.config import Settings
from app.schemas.url import CreateURLRequest, CreateURLResponse
from app.services.url import URLService

router = APIRouter()
redirect_router = APIRouter()


def get_settings() -> Settings:
    return Settings()


@router.post("/urls",response_model=CreateURLResponse, status_code=201)
async def create_url(
    request: CreateURLRequest, 
    service: URLService = Depends(get_url_service),
    settings: Settings = Depends(get_settings),
    ) -> CreateURLResponse:

    try:
        url = await service.create_url(
            original_url=str(request.original_url),
            expires_at=request.expires_at
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    return CreateURLResponse(
        original_url=url.original_url,
        short_code=url.short_code,
        short_url=f"{settings.base_url.rstrip('/')}/{url.short_code}",
    )


@redirect_router.get("/{short_code}")
async def redirect_to_url(
    short_code: str, 
    service: URLService = Depends(get_url_service),
    ) -> RedirectResponse:

    url = await service.get_url(short_code)
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(
        url=url.original_url,
        status_code=307,
    )
