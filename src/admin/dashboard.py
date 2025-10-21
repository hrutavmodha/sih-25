from fastapi import HTTPException
from models.admin.dashboard import DashboardResponse 
from database import supabase
from . import router

# ------------------------------
# ADMIN SIDE - DASHBOARD ENDPOINT
# ------------------------------
@router.get("/dashboard", response_model=DashboardResponse)
async def get_admin_dashboard():
    """
    GET /admin/dashboard
    Returns dashboard statistics from Supabase.
    """
    try:
        # Fetch total users
        students_data = supabase.table("students").select("id", count="exact").execute()
        total_users = students_data.count or 0

        # Fetch total FAQs
        faqs_data = supabase.table("faqs").select("id", count="exact").execute()
        total_faqs = faqs_data.count or 0

        # Fetch solved FAQs
        solved_faqs_data = supabase.table("faqs").select("id", count="exact").eq("status", "solved").execute()
        solved_faqs = solved_faqs_data.count or 0

        # Fetch unsolved FAQs
        unsolved_faqs_data = supabase.table("faqs").select("id", count="exact").eq("status", "unsolved").execute()
        unsolved_faqs_count = unsolved_faqs_data.count or 0

        # Fetch unsolved queries
        unsolved_queries_data = supabase.table("unsolved_queries").select("id", count="exact").execute()
        unsolved_queries = unsolved_queries_data.count or 0

        # Combine unsolved FAQs + queries
        unsolved_faqs = unsolved_faqs_count + unsolved_queries

        # Calculate success rate
        total_queries = solved_faqs + unsolved_faqs
        success_rate = (solved_faqs / total_queries * 100) if total_queries > 0 else 0

        # Return final result
        return DashboardResponse(
            total_users=total_users,
            total_faqs=total_faqs,
            solved_faqs=solved_faqs,
            unsolved_faqs=unsolved_faqs,
            success_rate=round(success_rate, 2)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
