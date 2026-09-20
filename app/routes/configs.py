from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.dependencies.auth import require_role
from app.models.user import DailySchedule, FeeConfig
from app.schemas.config import BatchScheduleUpdateRequest, DailyScheduleResponse, FeeConfigUpdateRequest, FeeConfigResponse

router = APIRouter(prefix="/api/configs", tags=["Configurations"])

@router.get("/schedules", response_model=List[DailyScheduleResponse])
def get_daily_schedules(db: Session = Depends(get_db), current_user = Depends(require_role(["admin", "teacher", "accountant"]))):
    return db.query(DailySchedule).all()

@router.post("/schedules")
def update_daily_schedules(payload: BatchScheduleUpdateRequest, db: Session = Depends(get_db), current_user = Depends(require_role(["admin"]))):
    try:
        db.query(DailySchedule).delete()
        for item in payload.schedules:
            new_slot = DailySchedule(
                class_name=item.class_name,
                period=item.period,
                subject=item.subject,
                teacher_id=item.teacher_id
            )
            db.add(new_slot)
        db.commit()
        return {"status": "success", "message": "Daily routines updated."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/schedules/my", response_model=List[DailyScheduleResponse])
def get_my_daily_schedules(
    db: Session = Depends(get_db), 
    current_user = Depends(require_role(["teacher"]))
):
    return db.query(DailySchedule).filter(DailySchedule.teacher_id == current_user.id).order_by(DailySchedule.period.asc()).all()



@router.get("/fees", response_model=List[FeeConfigResponse])
def get_fee_configs(db: Session = Depends(get_db), current_user = Depends(require_role(["admin", "accountant"]))):
    return db.query(FeeConfig).all()

@router.put("/fees/{class_name}", response_model=FeeConfigResponse)
def update_class_fees(class_name: str, payload: FeeConfigUpdateRequest, db: Session = Depends(get_db), current_user = Depends(require_role(["admin"]))):
    fees = db.query(FeeConfig).filter(FeeConfig.class_name == class_name).first()
    if not fees:
        raise HTTPException(status_code=404, detail="Class configuration target not found.")
    fees.monthly_fee = payload.monthly_fee
    fees.admission_fee = payload.admission_fee
    db.commit()
    db.refresh(fees)
    return fees