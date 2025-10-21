from fastapi import HTTPException, Path
from models.admin.unsolvedQuery import UnsolvedQuery, UnsolvedQueryUpdate 
from database import supabase
from datetime import datetime
from . import router

# ------------------------------
# 1️⃣ GET - List all unsolved queries
# ------------------------------
@router.get("/unsolved", response_model=list[UnsolvedQuery])
async def list_unsolved_queries():
    """
    GET /admin/unsolved
    Returns all unsolved (unreviewed) student queries.
    """
    try:
        response = (
            supabase.table("unsolved_queries")
            .select("*")
            .eq("reviewed", False)
            .order("created_at", desc=True)
            .execute()
        )
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------
# 2️⃣ PUT - Mark query as reviewed or solved (with automatic chat linking)
# ------------------------------
@router.put("/unsolved/{id}")
async def update_unsolved_query(id: int = Path(...), data: UnsolvedQueryUpdate = None):
    """
    PUT /admin/unsolved/{id}
    Marks a query as reviewed or solved.
    If solved=True → adds to FAQs + updates student's chat history.
    """
    try:
        # Step 1️⃣ — Fetch the original query
        query_data = supabase.table("unsolved_queries").select("*").eq("id", id).execute()
        if not query_data.data:
            raise HTTPException(status_code=404, detail="Query not found")
        query_item = query_data.data[0]

        student_id = query_item["student_id"]
        query_text = query_item["query_text"]

        # Step 2️⃣ — Mark query as reviewed
        supabase.table("unsolved_queries").update({"reviewed": data.reviewed}).eq("id", id).execute()

        # Step 3️⃣ — If admin solved it, move to FAQs and update chat log
        if data.solved:
            answer_text = data.answer or "Answer added by admin"

            # ➕ Add to FAQs
            faq_data = {
                "question": query_text,
                "answer": answer_text,
                "source_type": "text",
                "created_by": 1,  # Replace with logged-in admin ID if available
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "status": "solved"
            }
            faq_insert = supabase.table("faqs").insert(faq_data).execute()

            # ✅ Update the student's chat history (auto bot reply)
            chat_record = (
                supabase.table("chat_logs")
                .select("id")
                .eq("student_id", student_id)
                .eq("query_text", query_text)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )

            if chat_record.data:
                chat_id = chat_record.data[0]["id"]
                supabase.table("chat_logs").update(
                    {
                        "bot_response": answer_text,
                        "status": "solved",
                        "updated_at": datetime.utcnow().isoformat()
                    }
                ).eq("id", chat_id).execute()
            else:
                # If no chat record exists, create one for student
                chat_log = {
                    "student_id": student_id,
                    "query_text": query_text,
                    "bot_response": answer_text,
                    "status": "solved",
                    "created_at": datetime.utcnow().isoformat(),
                }
                supabase.table("chat_logs").insert(chat_log).execute()

            # 🧹 Clean up unsolved_queries
            supabase.table("unsolved_queries").delete().eq("id", id).execute()

            return {
                "message": "Query solved, added to FAQs, and student chat updated.",
                "linked_to_student_chat": True
            }

        # If only reviewed, not solved
        return {"message": "Query marked as reviewed", "linked_to_student_chat": False}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
