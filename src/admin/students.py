from fastapi import HTTPException, Path
from models.admin.students import StudentBase, StudentResponse, StudentUpdate
from database import supabase
from hashlib import sha256
from . import router

@router.post("/students", response_model=StudentResponse)
async def add_student(student: StudentBase):
    """
    POST /admin/students
    Add a new student.
    """
    try:
        # Hash password (simple SHA256 for now)
        hashed_password = sha256(student.password.encode()).hexdigest()

        data = {
            "name": student.name,
            "email": student.email,
            "password": hashed_password,
            "department": student.department,
            "enrollment_no": student.enrollment_no,
            "role": "student",
            "status": "active",
        }

        response = supabase.table("students").insert(data).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to add student.")

        return response.data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------------
# 2️⃣ List All Students
# ------------------------------
@router.get("/students", response_model=list[StudentResponse])
async def list_students():
    """
    GET /admin/students
    Returns all students.
    """
    try:
        response = supabase.table("students").select(
            "id, name, email, department, enrollment_no, role, status"
        ).order("id", desc=True).execute()
        return response.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------------
# 3️⃣ Update Student
# ------------------------------
@router.put("/students/{id}", response_model=StudentResponse)
async def update_student(id: int = Path(...), student: StudentUpdate = None):
    """
    PUT /admin/students/{id}
    Update student details.
    """
    try:
        update_data = {k: v for k, v in student.model_dump().items() if v is not None}

        if "password" in update_data:
            update_data["password"] = sha256(update_data["password"].encode()).hexdigest()

        response = supabase.table("students").update(update_data).eq("id", id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Student not found.")
        return response.data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------------
# 4️⃣ Delete Student
# ------------------------------
@router.delete("/students/{id}")
async def delete_student(id: int = Path(...)):
    """
    DELETE /admin/students/{id}
    Delete a student.
    """
    try:
        response = supabase.table("students").delete().eq("id", id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Student not found.")
        return {"message": "Student deleted successfully", "deleted_id": id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
