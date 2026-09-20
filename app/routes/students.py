# admin upload csv file and update student records

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.student import StudentResponse, StudentCreateRequest, StudentUpdateRequest, ImportTextRequest
from app.services import student_service
from app.dependencies.auth import require_role

router = APIRouter(prefix="/api/students", tags=["Students"])

@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(request: StudentCreateRequest, db: Session = Depends(get_db), current_user = Depends(require_role(["admin"]))):
    try:
        return student_service.create_student(db, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{regd}", response_model=StudentResponse)
def update_student(regd: str, request: StudentUpdateRequest, db: Session = Depends(get_db), current_user = Depends(require_role(["admin"]))):
    try:
        return student_service.update_student(db, regd, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[StudentResponse])
def get_all_students(db: Session = Depends(get_db), current_user = Depends(require_role(["admin", "teacher", "accountant"]))):
    return student_service.get_all_students(db)

@router.post("/import")
def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db), current_user = Depends(require_role(["admin"]))):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    try:
        content = file.file.read().decode("utf-8")
        return student_service.import_students_csv(db, content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")



@router.post("/import-text")
def import_csv_text(
    request: ImportTextRequest,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin"]))
):
    try:
        return student_service.import_students_csv(db, request.csv_text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV text: {str(e)}")