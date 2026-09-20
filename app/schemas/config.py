# For admin configuration of daily schedule and fee structure

from pydantic import BaseModel, Field
from typing import Optional, List

class DailyScheduleItem(BaseModel):
    class_name: str
    period: int
    subject: str
    teacher_id: Optional[int] = None

class BatchScheduleUpdateRequest(BaseModel):
    schedules: List[DailyScheduleItem]

class DailyScheduleResponse(BaseModel):
    class_name: str
    period: int
    subject: str
    teacher_id: Optional[int] = None

    class Config:
        from_attributes = True

class FeeConfigUpdateRequest(BaseModel):
    monthly_fee: float = Field(..., ge=0)
    admission_fee: float = Field(..., ge=0)

class FeeConfigResponse(BaseModel):
    class_name: str
    monthly_fee: float
    admission_fee: float

    class Config:
        from_attributes = True