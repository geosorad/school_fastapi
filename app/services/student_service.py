# admin upload csv student lost and update student records

import csv
import io
from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentCreateRequest, StudentUpdateRequest

def create_student(db: Session, request: StudentCreateRequest) -> Student:
    existing = db.query(Student).filter(Student.regd == request.regd).first()
    if existing:
        raise ValueError(f"Registration number '{request.regd}' already exists.")
    new_student = Student(
        regd=request.regd,
        roll_no=request.roll_no,
        name=request.name,
        class_name=request.class_name,
        dob=request.dob,
        address=request.address,
        contact_no=request.contact_no
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

def update_student(db: Session, regd: str, request: StudentUpdateRequest) -> Student:
    student = db.query(Student).filter(Student.regd == regd).first()
    if not student:
        raise ValueError("Student record not found.")
    
    if request.name is not None:
        student.name = request.name
    if request.roll_no is not None:
        student.roll_no = request.roll_no
    if request.class_name is not None:
        student.class_name = request.class_name
    if request.dob is not None:
        student.dob = request.dob
    if request.address is not None:
        student.address = request.address
    if request.contact_no is not None:
        student.contact_no = request.contact_no

    db.commit()
    db.refresh(student)
    return student

def get_all_students(db: Session):
    return db.query(Student).all()

def import_students_csv(db: Session, csv_content: str):
    f = io.StringIO(csv_content)
    # Automatically handles headers with spaces or different casing
    reader = csv.DictReader(f)
    
    success_count = 0
    skipped_count = 0
    errors = []
    
    for index, row in enumerate(reader, start=1):
        # Normalize header keys and values
        clean_row = {k.strip().lower(): (v.strip() if v else None) for k, v in row.items()}
        
        regd = clean_row.get("regd") or clean_row.get("registration") or clean_row.get("regd no") or clean_row.get("regd_no")
        name = clean_row.get("name") or clean_row.get("student name") or clean_row.get("student_name")
        
        if not regd or not name:
            errors.append(f"Row {index}: Missing required fields ('regd' or 'name')")
            continue
            
        existing = db.query(Student).filter(Student.regd == regd).first()
        if existing:
            skipped_count += 1
            continue
        
        student = Student(
            regd=regd,
            roll_no=clean_row.get("roll_no") or clean_row.get("roll no") or clean_row.get("roll") or clean_row.get("roll_num"),
            name=name,
            class_name=clean_row.get("class") or clean_row.get("class_name") or clean_row.get("grade"),
            dob=clean_row.get("dob") or clean_row.get("date of birth") or clean_row.get("date_of_birth"),
            address=clean_row.get("address"),
            contact_no=clean_row.get("contact") or clean_row.get("contact no") or clean_row.get("contact_no") or clean_row.get("phone")
        )
        db.add(student)
        success_count += 1
        
    db.commit()
    return {"success_count": success_count, "skipped_count": skipped_count, "errors": errors}