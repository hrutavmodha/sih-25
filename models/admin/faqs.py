from pydantic import BaseModel

class FAQBase(BaseModel):
    question: str
    answer: str
    source_type: str
    source_file: str | None = None
    created_by: int
    status: str = "pending"  # solved | unsolved | pending


class FAQUpdate(BaseModel):
    question: str | None = None
    answer: str | None = None
    status: str | None = None


class FAQResponse(BaseModel):
    id: int
    question: str
    answer: str
    source_type: str
    source_file: str | None
    created_by: int
    created_at: str
    updated_at: str | None
    status: str
