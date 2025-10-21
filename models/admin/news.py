from pydantic import BaseModel

class NewsBase(BaseModel):
    title: str
    content: str
    created_by: int

class NewsUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class NewsResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: str
    updated_at: str | None
    created_by: int