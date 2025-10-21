from pydantic import BaseModel, EmailStr

class StudentBase(BaseModel):
    name: str
    email: EmailStr
    password: str
    department: str
    enrollment_no: str

class StudentUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    department: str | None = None
    enrollment_no: str | None = None
    status: str | None = None

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    department: str
    enrollment_no: str
    role: str
    status: str