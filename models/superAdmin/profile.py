from pydantic import BaseModel, EmailStr

class SuperAdminResponse(BaseModel):
    id: int
    name: str
    email: str
    contact: str | None = None
    role: str
    status: str

class SuperAdminUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    contact: str | None = None