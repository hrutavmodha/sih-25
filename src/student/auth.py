from fastapi import APIRouter, HTTPException
from models.student.auth import TokenResponse, StudentLogin
from database import supabase
from hashlib import sha256
from os import getenv
import jwt
from datetime import datetime, timedelta
from . import router 

# ------------------------------
# JWT SECRET (use environment variable in production)
# ------------------------------
JWT_SECRET = getenv("JWT_SECRET", "supersecretkey")
JWT_ALGORITHM = "HS256"

# ------------------------------
# Utility Functions
# ------------------------------
def create_jwt_token(data: dict):
    """Generate JWT token with 1-hour expiration"""
    payload = data.copy()
    payload["exp"] = datetime.now(datetime.timezone.utc) + timedelta(hours=1)
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

# ------------------------------
# 1️⃣ Student Login API
# ------------------------------
@router.post("/login", response_model=TokenResponse)
async def student_login(credentials: StudentLogin):
    """
    POST /auth/login
    Logs in a student using email and password.
    Returns JWT token on success.
    """
    try:
        # Hash incoming password (same as stored)
        hashed_password = sha256(credentials.password.encode()).hexdigest()

        # Query Supabase for the student
        response = supabase.table("students").select("*").eq("email", credentials.email).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Invalid email or password")

        student = response.data[0]

        # Compare hashed passwords
        if student["password"] != hashed_password:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if student["status"] != "active":
            raise HTTPException(status_code=403, detail="Account inactive. Contact admin.")

        # Generate JWT token
        token = create_jwt_token({
            "student_id": student["id"],
            "email": student["email"],
            "role": student.get("role", "student")
        })

        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
