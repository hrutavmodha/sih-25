from fastapi import HTTPException, UploadFile, File, Form, Path
from models.admin.faqs import FAQResponse, FAQUpdate
from database import supabase
from datetime import datetime
from os import path
import tempfile
from . import router

# ------------------------------
# 1️⃣ Add FAQ (Manual or via PDF Upload)
# ------------------------------
@router.post("/faqs", response_model=FAQResponse)
async def add_faq(
    question: str = Form(None),
    answer: str = Form(None),
    source_type: str = Form("manual"),
    created_by: int = Form(...),
    file: UploadFile | None = File(None)
):
    """
    POST /admin/faqs
    Add FAQ manually or via PDF.
    """

    try:
        if source_type == "pdf" and file:
            # Save PDF temporarily
            temp_dir = tempfile.gettempdir()
            file_path = path.join(temp_dir, file.filename)
            with open(file_path, "wb") as f:
                f.write(await file.read())

            # In a real app: extract QnA from PDF and save to DB.
            # For now, just mock this behavior:
            question_text = "Extracted question from PDF"
            answer_text = "Extracted answer from PDF"
            source_file = file.filename

        else:
            question_text = question
            answer_text = answer
            source_file = None

        data = {
            "question": question_text,
            "answer": answer_text,
            "source_type": source_type,
            "source_file": source_file,
            "created_by": created_by,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        response = supabase.table("faqs").insert(data).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to insert FAQ")

        return response.data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------
# 2️⃣ Get All FAQs
# ------------------------------
@router.get("/faqs", response_model=list[FAQResponse])
async def get_all_faqs():
    """
    GET /admin/faqs
    List all FAQs.
    """
    try:
        response = supabase.table("faqs").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------
# 3️⃣ Update FAQ
# ------------------------------
@router.put("/faqs/{id}", response_model=FAQResponse)
async def update_faq(id: int = Path(...), faq: FAQUpdate = None):
    """
    PUT /admin/faqs/{id}
    Update FAQ question, answer, or status.
    """
    try:
        update_data = {k: v for k, v in faq.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow().isoformat()

        response = supabase.table("faqs").update(update_data).eq("id", id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="FAQ not found")

        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------
# 4️⃣ Delete FAQ
# ------------------------------
@router.delete("/faqs/{id}")
async def delete_faq(id: int = Path(...)):
    """
    DELETE /admin/faqs/{id}
    Delete a specific FAQ.
    """
    try:
        response = supabase.table("faqs").delete().eq("id", id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="FAQ not found")
        return {"message": "FAQ deleted successfully", "deleted_id": id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
