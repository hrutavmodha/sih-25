from fastapi import HTTPException, Path
from models.admin.news import NewsBase, NewsResponse, NewsUpdate
from database import supabase
from datetime import datetime
from . import router

# ------------------------------
# ADMIN SIDE - LATEST NEWS APIs
# ------------------------------

# ✅ 1️⃣ Add News
@router.post("/news", response_model=NewsResponse)
async def add_news(news: NewsBase):
    """
    POST /admin/news
    Adds a new news entry.
    """
    try:
        data = {
            "title": news.title,
            "content": news.content,
            "created_by": news.created_by,
            "created_at": datetime.now(datetime.timezone.utc).isoformat(),
            "updated_at": datetime.now(datetime.timezone.utc).isoformat(),
        }

        response = supabase.table("news").insert(data).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to insert news.")
        return response.data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ 2️⃣ List All News
@router.get("/news", response_model=list[NewsResponse])
async def list_all_news():
    """
    GET /admin/news
    Returns all news entries.
    """
    try:
        response = (
            supabase.table("news")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ 3️⃣ Update News
@router.put("/news/{id}", response_model=NewsResponse)
async def update_news(
    id: int = Path(..., description="News ID to update"), news: NewsUpdate = None
):
    """
    PUT /admin/news/{id}
    Updates a specific news item.
    """
    try:
        update_data = {k: v for k, v in news.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow().isoformat()

        response = supabase.table("news").update(update_data).eq("id", id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="News not found.")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ 4️⃣ Delete News
@router.delete("/news/{id}")
async def delete_news(id: int = Path(..., description="News ID to delete")):
    """
    DELETE /admin/news/{id}
    Deletes a specific news entry.
    """
    try:
        response = supabase.table("news").delete().eq("id", id).execute()
        if not response.data:
            raise HTTPException(
                status_code=404, detail="News not found or already deleted."
            )
        return {"message": "News deleted successfully", "deleted_id": id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
