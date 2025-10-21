from pydantic import BaseModel

class DashboardResponse(BaseModel):
    total_users: int
    total_faqs: int
    solved_faqs: int
    unsolved_faqs: int
    success_rate: float