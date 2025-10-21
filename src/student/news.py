from fastapi import APIRouter, HTTPException
from models.student.news import NewsResponse
from database import supabase
from . import router 

# ------------------------------
# 1️⃣ GET - Fetch all active news
# ------------------------------
@router.get("/news", response_model=list[NewsResponse])
async def get_student_news():
    """
    GET /student/news
    Returns all active news (latest first).
    """
    try:
        # Fetch news sorted by created_at (newest first)
        response = (
            supabase.table("news")
            .select("id, title, content, created_by, created_at, updated_at")
            .order("created_at", desc=True)
            .execute()
        )

        if not response.data:
            return []  # No news yet

        return response.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
