from pydantic import BaseModel, HttpUrl

class CreateURLRequest(BaseModel):
    original_url: HttpUrl


class CreateURLResponse(BaseModel):
    original_url: HttpUrl
    short_code: str
    short_url: str
