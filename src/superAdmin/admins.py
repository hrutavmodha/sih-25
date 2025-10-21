from fastapi import HTTPException, Path, Depends, Header
from models.superAdmin.admins import AdminBase, AdminResponse, AdminUpdate
from database import supabase
from os import getenv
from hashlib import sha256
import jwt
from . import router

# ------------------------------
# JWT SETTINGS
# ------------------------------
JWT_SECRET = getenv("JWT_SECRET", "supersecretkey")  # ⚠️ Replace in production
JWT_ALGORITHM = "HS256"

# ------------------------------
# 🔒 Token Verification
# ------------------------------
def verify_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def verify_super_admin(decoded=Depends(verify_token)):
    """Allow only super_admin"""
    if decoded.get("role") != "super_admin":
        raise HTTPException(status_code=403, detail="Access denied — Super Admins only")
    return decoded


def verify_admin_or_super(decoded=Depends(verify_token)):
    """Allow admin or super_admin"""
    if decoded.get("role") not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Access denied — Admin or Super Admin only")
    return decoded

# ------------------------------
# 1️⃣ Add Admin — Super Admin Only
# ------------------------------
@router.post("/admins", response_model=AdminResponse, dependencies=[Depends(verify_super_admin)])
async def add_admin(admin: AdminBase):
    """
    POST /super-admin/admins
    Only Super Admins can add new admins.
    """
    try:
        hashed_password = sha256(admin.password.encode()).hexdigest()
        data = {
            "name": admin.name,
            "email": admin.email,
            "password": hashed_password,
            "role": admin.role,
            "status": admin.status,
        }

        response = supabase.table("admins").insert(data).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to add admin.")

        return response.data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------
# 2️⃣ Get All Admins — Admins + Super Admins
# ------------------------------
@router.get("/admins", response_model=list[AdminResponse], dependencies=[Depends(verify_admin_or_super)])
async def list_admins():
    """
    GET /super-admin/admins
    Accessible by Admins and Super Admins.
    """
    try:
        response = supabase.table("admins").select("id, name, email, role, status").order("id", desc=True).execute()
        return response.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------
# 3️⃣ Update Admin — Admins + Super Admins
# ------------------------------
@router.put("/admins/{id}", response_model=AdminResponse, dependencies=[Depends(verify_admin_or_super)])
async def update_admin(id: int = Path(...), admin: AdminUpdate = None):
    """
    PUT /super-admin/admins/{id}
    Accessible by Admins and Super Admins.
    """
    try:
        update_data = {k: v for k, v in admin.dict().items() if v is not None}

        if "password" in update_data:
            update_data["password"] = sha256(update_data["password"].encode()).hexdigest()

        response = supabase.table("admins").update(update_data).eq("id", id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Admin not found.")

        return response.data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------
# 4️⃣ Delete Admin — Super Admin Only
# ------------------------------
@router.delete("/admins/{id}", dependencies=[Depends(verify_super_admin)])
async def delete_admin(id: int = Path(...)):
    """
    DELETE /super-admin/admins/{id}
    Only Super Admins can delete admins.
    """
    try:
        response = supabase.table("admins").delete().eq("id", id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Admin not found or already deleted.")
        return {"message": "Admin deleted successfully", "deleted_id": id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
