from pydantic import BaseModel

class UnsolvedQuery(BaseModel):
    id: int
    student_id: int
    query_text: str
    created_at: str
    reviewed: bool


class UnsolvedQueryUpdate(BaseModel):
    reviewed: bool = True
    solved: bool | None = None  # optional, if marking solved
    answer: str | None = None   # optional, if moving to FAQs
