from datetime import datetime

from pydantic import BaseModel, HttpUrl, field_validator


class CreateURLRequest(BaseModel):
    original_url: HttpUrl
    expires_at: datetime | None = None

    @field_validator("expires_at")
    @classmethod
    def validate_expires_at(cls, value: datetime | None) -> datetime | None:
        if value is not None and value.tzinfo is None:
            raise ValueError("Expiration date must be timezone-aware")

        return value


class CreateURLResponse(BaseModel):
    original_url: HttpUrl
    short_code: str
    short_url: str
