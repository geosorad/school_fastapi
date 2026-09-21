import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.dependencies.auth import require_role
from app.models.user import User
from app.schemas.academic import (
    TopicCreate, TopicResponse, BatchRatingsRequest, 
    AssessmentResponse, SyncPushPayload
)
from app.services import academic_service

from app.schemas.academic import TodayStudentRatingsGroup


router = APIRouter(prefix="/api/academics", tags=["Academics"])

@router.get("/topics", response_model=List[TopicResponse])
def get_topics(
    db: Session = Depends(get_db), 
    current_user: User = Depends(require_role(["teacher", "admin"]))
):
    return academic_service.get_topics_for_teacher(db, current_user.id)

@router.post("/topics", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
def create_topic(
    request: TopicCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(require_role(["teacher", "admin"]))
):
    return academic_service.create_topic(db, current_user.id, request)

@router.get("/ratings", response_model=List[AssessmentResponse])
def get_ratings(
    topic_id: str, 
    criterion: str, 
    assessment_date: Optional[str] = None,
    db: Session = Depends(get_db), 
    current_user: User = Depends(require_role(["teacher", "admin"]))
):
    return academic_service.get_ratings(db, topic_id, criterion, assessment_date)

@router.post("/ratings/batch")
def save_batch_ratings(
    request: BatchRatingsRequest, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(require_role(["teacher", "admin"]))
):
    try:
        academic_service.upsert_batch_ratings(db, current_user.id, request)
        return {"status": "success", "message": "Ratings committed successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sync")
def sync_push(
    payload: SyncPushPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["teacher", "admin"]))
):
    try:
        for topic_req in payload.topics:
            academic_service.create_topic(db, current_user.id, topic_req)
        for batch in payload.ratings_batches:
            academic_service.upsert_batch_ratings(db, current_user.id, batch)
        return {"status": "success", "message": "Sync completed."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/ratings/today", response_model=List[TodayStudentRatingsGroup])
def get_today_ratings(
    date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    target_date = date or datetime.utcnow().strftime("%Y-%m-%d")
    return academic_service.get_today_ratings_grouped(db, target_date)


@router.get("/ratings/by-date", response_model=List[TodayStudentRatingsGroup])
@router.get("/ratings/today", response_model=List[TodayStudentRatingsGroup])
def get_ratings_by_date(
    date: str, # Accepts BS date string e.g. "2083-06-05"
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    return academic_service.get_today_ratings_grouped(db, date)