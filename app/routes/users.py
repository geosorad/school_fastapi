from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.user import UserResponse, TeacherCreateRequest, AccountantCreateRequest, StaffUpdateRequest
from app.dependencies.auth import require_role
from app.models.user import User
from app.services import user_service

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/teachers", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def add_teacher(request: TeacherCreateRequest, db: Session = Depends(get_db), current_user: User = Depends(require_role(["admin"]))):
    try:
        return user_service.create_teacher(db, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/accountants", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def add_accountant(request: AccountantCreateRequest, db: Session = Depends(get_db), current_user: User = Depends(require_role(["admin"]))):
    try:
        return user_service.create_accountant(db, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{user_id}", response_model=UserResponse)
def update_staff_member(user_id: int, request: StaffUpdateRequest, db: Session = Depends(get_db), current_user: User = Depends(require_role(["admin"]))):
    try:
        return user_service.update_staff(db, user_id, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/teachers", response_model=List[UserResponse])
def get_teachers(db: Session = Depends(get_db), current_user: User = Depends(require_role(["admin", "accountant"]))):
    return user_service.get_all_users_by_role(db, "teacher")

@router.get("/accountants", response_model=List[UserResponse])
def get_accountants(db: Session = Depends(get_db), current_user: User = Depends(require_role(["admin"]))):
    return user_service.get_all_users_by_role(db, "accountant")