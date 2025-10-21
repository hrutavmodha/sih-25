from fastapi import APIRouter

# Create a single APIRouter for the entire "student" module
router = APIRouter(
    prefix = "/student",
    tags = [
        "Student Authentication",
        "Student Chatbot",
        "Student APIs",
        "Student News"   
    ]
)

# Import route modules to register the endpoints
from . import auth
from . import chat
from . import main
from . import news