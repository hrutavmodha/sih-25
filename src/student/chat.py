from fastapi import APIRouter, HTTPException, Path
from models.student.chat import ChatRequest, ChatResponse
from database import supabase
from datetime import datetime, timezone
from . import router 

# ------------------------------
# 1️⃣ POST /student/chat
# ------------------------------
@router.post("/chat", response_model=ChatResponse)
async def send_chat_query(chat: ChatRequest):
    """
    POST /student/chat
    Handles student query → returns FAQ match or fallback reply.
    Automatically stores logs and unsolved queries.
    """
    try:
        query_text = chat.query_text.strip()
        if not query_text:
            raise HTTPException(status_code=400, detail="Query text cannot be empty.")

        # Step 1️⃣: Search FAQs for a matching question
        faqs = supabase.table("faqs").select("id, question, answer").execute()
        bot_response = None
        matched_faq_id = None

        for faq in faqs.data:
            if query_text.lower() in faq["question"].lower():
                bot_response = faq["answer"]
                matched_faq_id = faq["id"]
                break

        # Step 2️⃣: If match found → mark as solved
        if bot_response:
            status = "solved"
        else:
            # No match found → fallback response
            bot_response = (
                "I'm not sure about that yet, but our admin will review your question soon."
            )
            status = "unsolved"

            # Step 3️⃣: Save to unsolved_queries table
            unsolved_data = {
                "student_id": chat.student_id,
                "query_text": chat.query_text,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "reviewed": False,
            }
            supabase.table("unsolved_queries").insert(unsolved_data).execute()

        # Step 4️⃣: Log the chat in chat_logs table
        chat_log = {
            "student_id": chat.student_id,
            "query_text": query_text,
            "detected_language": chat.detected_language,
            "bot_response": bot_response,
            "faq_id": matched_faq_id,
            "status": status,
            "created_at": datetime.utcnow().isoformat(),
        }
        supabase.table("chat_logs").insert(chat_log).execute()

        # Step 5️⃣: Return the bot response
        return {
            "query_text": query_text,
            "bot_response": bot_response,
            "status": status,
            "created_at": chat_log["created_at"],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------
# 2️⃣ GET /student/chat/{id}
# ------------------------------
@router.get("/chat/{student_id}", response_model=list[ChatResponse])
async def get_chat_history(student_id: int = Path(...)):
    """
    GET /student/chat/{id}
    Returns all previous chat logs for the given student.
    """
    try:
        response = (
            supabase.table("chat_logs")
            .select("query_text, bot_response, status, created_at")
            .eq("student_id", student_id)
            .order("created_at", desc=True)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=404, detail="No chat history found for this student.")

        return response.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
