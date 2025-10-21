from fastapi import APIRouter, HTTPException, Depends, Header
from models.superAdmin.profile import SuperAdminResponse, SuperAdminUpdate
from database import supabase
from os import getenv
from jwt import decode
from . import router

# ------------------------------
# JWT SETTINGS
# ------------------------------
JWT_SECRET = getenv("JWT_SECRET", "supersecretkey")  # ⚠️ Replace with a secure secret
JWT_ALGORITHM = "HS256"

# ------------------------------
# Token Verification
# ------------------------------
def verify_token(authorization: str = Header(...)):
    """
    Verifies the JWT token from Authorization header.
    """
    try:
        token = authorization.split(" ")[1]
        decoded = decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def verify_super_admin(decoded=Depends(verify_token)):
    """
    Ensures only the Super Admin can access this route.
    """
    if decoded.get("role") != "super_admin":
        raise HTTPException(status_code=403, detail="Access denied — Super Admin only")
    return decoded

# ------------------------------
# 1️⃣ GET Super Admin Profile
# ------------------------------
@router.get("/profile", response_model=SuperAdminResponse, dependencies=[Depends(verify_super_admin)])
async def get_super_admin_profile():
    """
    GET /super-admin/profile
    Returns the super admin’s profile (role='super_admin').
    """
    try:
        response = supabase.table("admins").select("*").eq("role", "super_admin").execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Super Admin not found.")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------------
# 2️⃣ UPDATE Super Admin Profile
# ------------------------------
@router.put("/profile", response_model=SuperAdminResponse, dependencies=[Depends(verify_super_admin)])
async def update_super_admin_profile(update: SuperAdminUpdate):
    """
    PUT /super-admin/profile
    Update the Super Admin’s name, email, or contact.
    """
    try:
        update_data = {k: v for k, v in update.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields to update.")

        # Fetch the Super Admin
        response = supabase.table("admins").select("id").eq("role", "super_admin").execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Super Admin not found.")

        super_admin_id = response.data[0]["id"]

        # Update Super Admin info
        result = supabase.table("admins").update(update_data).eq("id", super_admin_id).execute()
        if not result.data:
            raise HTTPException(status_code=400, detail="Failed to update Super Admin profile.")

        return result.data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
