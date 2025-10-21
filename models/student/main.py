from pydantic import BaseModel

class HomeResponse(BaseModel):
    name: str
    department: str
    enrollment_no: str
    motivational_quote: str
    latest_news: list[dict]

class ChatRequest(BaseModel):
    student_id: int
    query_text: str
    detected_language: str | None = "en"

class ChatResponse(BaseModel):
    query_text: str
    bot_response: str
    status: str
    created_at: str

class NewsResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: str
    created_by: int