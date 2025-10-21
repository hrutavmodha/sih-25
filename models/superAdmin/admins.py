from pydantic import BaseModel, EmailStr

class AdminBase(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "admin"
    status: str = "active"

class AdminUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: str | None = None
    status: str | None = None

class AdminResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    status: str
