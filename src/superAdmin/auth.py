from fastapi import APIRouter, HTTPException
from models.superAdmin.auth import TokenResponse, AdminLogin
from database import supabase
from datetime import datetime, timedelta
import hashlib
import jwt
from os import getenv
from . import router

# ------------------------------
# JWT SETTINGS
# ------------------------------
JWT_SECRET = getenv("JWT_SECRET", "supersecretkey")  # ⚠️ Replace with a secure value in production
JWT_ALGORITHM = "HS256"

# ------------------------------
# Utility Function
# ------------------------------
def create_jwt_token(data: dict):
    """Generate JWT token with 2-hour expiration"""
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=2)
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

# ------------------------------
# 1️⃣ Super Admin / Admin Login
# ------------------------------
@router.post("/login", response_model=TokenResponse)
async def admin_login(credentials: AdminLogin):
    """
    POST /super-admin/auth/login
    Logs in an admin or super_admin.
    Returns a JWT token.
    """
    try:
        # Hash password for comparison
        hashed_password = hashlib.sha256(credentials.password.encode()).hexdigest()

        # Query Supabase for admin
        response = supabase.table("admins").select("*").eq("email", credentials.email).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Invalid email or password")

        admin = response.data[0]

        # Validate password
        if admin["password"] != hashed_password:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Check account status
        if admin["status"] != "active":
            raise HTTPException(status_code=403, detail="Account inactive")

        # Create JWT token
        token = create_jwt_token({
            "admin_id": admin["id"],
            "email": admin["email"],
            "role": admin["role"]
        })

        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
