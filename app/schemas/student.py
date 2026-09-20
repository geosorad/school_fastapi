from pydantic import BaseModel
from typing import Optional

class StudentCreateRequest(BaseModel):
    regd: str
    roll_no: Optional[str] = None
    name: str
    class_name: Optional[str] = None
    dob: Optional[str] = None
    address: Optional[str] = None
    contact_no: Optional[str] = None

class StudentUpdateRequest(BaseModel):
    roll_no: Optional[str] = None
    name: Optional[str] = None
    class_name: Optional[str] = None
    dob: Optional[str] = None
    address: Optional[str] = None
    contact_no: Optional[str] = None

class StudentResponse(BaseModel):
    regd: str
    roll_no: Optional[str] = None
    name: str
    class_name: Optional[str] = None
    dob: Optional[str] = None
    address: Optional[str] = None
    contact_no: Optional[str] = None

    class Config:
        from_attributes = True

class ImportTextRequest(BaseModel):
    csv_text: str