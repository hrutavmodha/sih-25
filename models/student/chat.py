from pydantic import BaseModel

class ChatRequest(BaseModel):
    student_id: int
    query_text: str
    detected_language: str | None = "en"

class ChatResponse(BaseModel):
    query_text: str
    bot_response: str
    status: str
    created_at: str
