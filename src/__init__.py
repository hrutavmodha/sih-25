from .admin import router as admin_router
from .student import router as student_router
from .superAdmin import router as super_admin_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(router = admin_router)
router.include_router(router = student_router)
router.include_router(router = super_admin_router)