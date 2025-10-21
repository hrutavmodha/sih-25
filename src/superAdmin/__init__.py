from fastapi import APIRouter

# Create a single APIRouter for the entire "superAdmin" module
router = APIRouter(
    prefix = "/super-admin",
    tags = [
        "Admins",
        "Super Admin Profile",
        "Super Admin Authentication"
    ]
)

# Import route modules to register the endpoints
from . import admins
from . import auth
from . import profile
