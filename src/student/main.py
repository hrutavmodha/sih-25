from fastapi import APIRouter, HTTPException, Path
from models.student.main import HomeResponse
from models.student.chat import ChatRequest, ChatResponse
from models.student.news import NewsResponse
from database import supabase
from datetime import datetime
from . import router 

# ------------------------------
# 1️⃣ GET /student/home/{id}
# ------------------------------
@router.get("/home/{student_id}", response_model=HomeResponse)
async def get_student_home(student_id: int = Path(...)):
    """
    Returns:
    - student details (name, department, enrollment_no)
    - motivational quote
    - latest 3 news items
    """
    try:
        # Fetch student details
        student_res = supabase.table("students").select(
            "name, department, enrollment_no"
        ).eq("id", student_id).execute()

        if not student_res.data:
            raise HTTPException(status_code=404, detail="Student not found")

        student = student_res.data[0]

        # Fetch latest news
        news_res = supabase.table("news").select(
            "id, title, content, created_at, created_by"
        ).order("created_at", desc=True).limit(3).execute()
        latest_news = news_res.data or []

        # Motivational quote (static for now)
        quote = "The future depends on what you do today. — Mahatma Gandhi"

        return {
            "name": student["name"],
            "department": student["department"],
            "enrollment_no": student["enrollment_no"],
            "motivational_quote": quote,
            "latest_news": latest_news
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------------
# 2️⃣ POST /student/chat
# ------------------------------
@router.post("/chat", response_model=ChatResponse)
async def send_student_chat(chat: ChatRequest):
    """
    Handles chat queries:
    - Checks if query matches FAQ
    - If matched -> solved
    - Else -> unsolved + stored in unsolved_queries
    """
    try:
        query_text = chat.query_text.strip()

        # Try to match FAQ
        faqs = supabase.table("faqs").select("id, question, answer").execute()
        bot_response = None
        matched_faq_id = None

        for faq in faqs.data:
            if query_text.lower() in faq["question"].lower():
                bot_response = faq["answer"]
                matched_faq_id = faq["id"]
                break

        if bot_response:
            status = "solved"
        else:
            bot_response = "I'm not sure, but our support team will review your question soon."
            status = "unsolved"

            # Log into unsolved_queries
            unsolved_data = {
                "student_id": chat.student_id,
                "query_text": query_text,
                "created_at": datetime.utcnow().isoformat(),
                "reviewed": False
            }
            supabase.table("unsolved_queries").insert(unsolved_data).execute()

        # Store in chat_logs
        chat_log = {
            "student_id": chat.student_id,
            "query_text": query_text,
            "detected_language": chat.detected_language,
            "bot_response": bot_response,
            "faq_id": matched_faq_id,
            "status": status,
            "created_at": datetime.utcnow().isoformat()
        }
        supabase.table("chat_logs").insert(chat_log).execute()

        return {
            "query_text": query_text,
            "bot_response": bot_response,
            "status": status,
            "created_at": chat_log["created_at"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------------
# 3️⃣ GET /student/chat/{id}
# ------------------------------
@router.get("/chat/{student_id}", response_model=list[ChatResponse])
async def get_student_chat(student_id: int = Path(...)):
    """
    Returns student's entire chat history.
    """
    try:
        res = supabase.table("chat_logs").select(
            "query_text, bot_response, status, created_at"
        ).eq("student_id", student_id).order("created_at", desc=True).execute()
        return res.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------------
# 4️⃣ GET /student/news
# ------------------------------
@router.get("/news", response_model=list[NewsResponse])
async def get_student_news():
    """
    Fetch all active news items for students.
    """
    try:
        res = supabase.table("news").select(
            "id, title, content, created_at, created_by"
        ).order("created_at", desc=True).execute()
        return res.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
