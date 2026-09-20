from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str
    name: str
    email: str
    id: int

class TeacherCreateRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    name: str
    base_salary: Optional[float] = None
    qualification: Optional[str] = None
    bank_account_no: Optional[str] = None
    joining_date: Optional[str] = None  # String for BS dates (e.g. "2080-05-15")
    left_date: Optional[str] = None

class AccountantCreateRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    name: str
    base_salary: Optional[float] = None
    qualification: Optional[str] = None
    bank_account_no: Optional[str] = None
    joining_date: Optional[str] = None
    left_date: Optional[str] = None

class StaffUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)  # Optional password change
    base_salary: Optional[float] = None
    qualification: Optional[str] = None
    bank_account_no: Optional[str] = None
    joining_date: Optional[str] = None
    left_date: Optional[str] = None

class TeacherProfileResponse(BaseModel):
    base_salary: Optional[float] = None
    qualification: Optional[str] = None
    bank_account_no: Optional[str] = None
    joining_date: Optional[str] = None
    left_date: Optional[str] = None

    class Config:
        from_attributes = True

class AccountantProfileResponse(BaseModel):
    base_salary: Optional[float] = None
    qualification: Optional[str] = None
    bank_account_no: Optional[str] = None
    joining_date: Optional[str] = None
    left_date: Optional[str] = None

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str
    is_active: bool
    teacher_profile: Optional[TeacherProfileResponse] = None
    accountant_profile: Optional[AccountantProfileResponse] = None

    class Config:
        from_attributes = True