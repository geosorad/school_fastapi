import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Optional

from starlette.exceptions import HTTPException
from app.models.academic import Topic, StudentAssessment
from app.schemas.academic import TopicCreate, BatchRatingsRequest, TopicUpdateRequest

from app.models.student import Student
from app.models.user import User

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


def get_today_ratings_grouped(db: Session, date_str: str) -> List[dict]:
    results = (
        db.query(
            StudentAssessment,
            Student.name.label("student_name"),
            Student.class_name.label("student_class"),
            Student.roll_no.label("student_roll"),
            Student.contact_no.label("student_contact"),
            Topic.title.label("topic_title"),
            Topic.subject.label("topic_subject"),
            User.name.label("teacher_name")
        )
        .join(Student, StudentAssessment.student_regd == Student.regd)
        .join(Topic, StudentAssessment.topic_id == Topic.id)
        .join(User, StudentAssessment.teacher_id == User.id)
        .filter(StudentAssessment.assessment_date == date_str)
        .order_by(Student.name.asc(), StudentAssessment.updated_at.desc())
        .all()
    )

    grouped = {}
    for row in results:
        regd = row.StudentAssessment.student_regd
        if regd not in grouped:
            grouped[regd] = {
                "student_regd": regd,
                "student_name": row.student_name,
                "class_name": row.student_class,
                "roll_no": row.student_roll,
                "contact_no": row.student_contact,
                "ratings": []
            }
        grouped[regd]["ratings"].append({
            "id": row.StudentAssessment.id,
            "teacher_id": row.StudentAssessment.teacher_id,
            "teacher_name": row.teacher_name,
            "subject": row.topic_subject,
            "topic_title": row.topic_title,
            "criterion": row.StudentAssessment.criterion,
            "rating": row.StudentAssessment.rating,
            "updated_at": row.StudentAssessment.updated_at
        })

    return list(grouped.values())


def update_topic_description(db: Session, topic_id: str, teacher_id: int, request: TopicUpdateRequest) -> Topic:
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found.")
    
    if topic.teacher_id != teacher_id:
        raise HTTPException(status_code=403, detail="You do not have permission to modify this topic.")

    # Topic name (title), class_name, and subject are strictly immutable once created
    topic.description = request.description
    db.commit()
    db.refresh(topic)
    return topic