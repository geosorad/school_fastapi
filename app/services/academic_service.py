import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.academic import Topic, StudentAssessment
from app.schemas.academic import TopicCreate, BatchRatingsRequest

def create_topic(db: Session, teacher_id: int, request: TopicCreate) -> Topic:
    topic_id = request.id or f"top_{uuid.uuid4().hex[:12]}"
    created_date = request.created_at or datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    existing = db.query(Topic).filter(Topic.id == topic_id).first()
    if existing:
        return existing

    new_topic = Topic(
        id=topic_id,
        teacher_id=teacher_id,
        class_name=request.class_name,
        subject=request.subject,
        title=request.title,
        description=request.description,
        created_at=created_date
    )
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic

def get_topics_for_teacher(db: Session, teacher_id: int) -> List[Topic]:
    return db.query(Topic).filter(Topic.teacher_id == teacher_id).order_by(Topic.created_at.desc()).all()

def upsert_batch_ratings(db: Session, teacher_id: int, request: BatchRatingsRequest):
    now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    for item in request.ratings:
        assessment_id = f"{item.student_regd}_{request.topic_id}_{request.criterion}_{request.assessment_date}"
        existing = db.query(StudentAssessment).filter(StudentAssessment.id == assessment_id).first()
        if existing:
            existing.rating = item.rating
            existing.updated_at = now_str
        else:
            record = StudentAssessment(
                id=assessment_id,
                topic_id=request.topic_id,
                student_regd=item.student_regd,
                criterion=request.criterion,
                rating=item.rating,
                assessment_date=request.assessment_date,
                teacher_id=teacher_id,
                updated_at=now_str
            )
            db.add(record)
    db.commit()

def get_ratings(db: Session, topic_id: str, criterion: str, assessment_date: Optional[str] = None):
    query = db.query(StudentAssessment).filter(
        StudentAssessment.topic_id == topic_id,
        StudentAssessment.criterion == criterion
    )
    if assessment_date:
        query = query.filter(StudentAssessment.assessment_date == assessment_date)
    return query.all()