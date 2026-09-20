from pydantic import BaseModel
from typing import Optional, List

class TopicCreate(BaseModel):
    id: Optional[str] = None
    class_name: str
    subject: str
    title: str
    description: Optional[str] = None
    created_at: Optional[str] = None

class TopicResponse(BaseModel):
    id: str
    teacher_id: int
    class_name: str
    subject: str
    title: str
    description: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True

class RatingItem(BaseModel):
    student_regd: str
    rating: float

class BatchRatingsRequest(BaseModel):
    topic_id: str
    criterion: str
    assessment_date: str # YYYY-MM-DD
    ratings: List[RatingItem]

class AssessmentResponse(BaseModel):
    id: str
    topic_id: str
    student_regd: str
    criterion: str
    rating: float
    assessment_date: str
    teacher_id: int
    updated_at: str

    class Config:
        from_attributes = True

class SyncPushPayload(BaseModel):
    topics: List[TopicCreate] = []
    ratings_batches: List[BatchRatingsRequest] = []