from pydantic import BaseModel

class NewsResponse(BaseModel):
    id: int
    title: str
    content: str
    created_by: int
    created_at: str
    updated_at: str | None = None