from fastapi import APIRouter

# Create a single APIRouter for the entire "admin" module
router = APIRouter(
    prefix = "/admin", 
    tags = [
        "Dashboard",
        "FAQs",
        "News",
        "Students",
        "Unsolved Queries"
    ]
)

# Import route modules to register the endpoints
from . import dashboard
from . import faqs
from . import news
from . import students
from . import unsolvedQuery