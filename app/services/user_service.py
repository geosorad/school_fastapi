from sqlalchemy.orm import Session
from app.models.user import User, TeacherProfile, AccountantProfile
from app.schemas.user import TeacherCreateRequest, AccountantCreateRequest, StaffUpdateRequest
from app.dependencies.auth import hash_password
from app.core.config import settings

def seed_default_admin(db: Session):
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin:
        default_admin = User(
            email=settings.DEFAULT_ADMIN_EMAIL,
            name="System Administrator",
            hashed_password=hash_password(settings.DEFAULT_ADMIN_PASSWORD),
            role="admin",
            is_active=True,
            token_version=1
        )
        db.add(default_admin)
        db.commit()
        db.refresh(default_admin)

def create_teacher(db: Session, request: TeacherCreateRequest) -> User:
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise ValueError("A user with this email already exists.")

    new_user = User(
        email=request.email,
        name=request.name,
        hashed_password=hash_password(request.password),
        role="teacher",
        is_active=True,
        token_version=1
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    teacher_profile = TeacherProfile(
        user_id=new_user.id,
        base_salary=request.base_salary,
        qualification=request.qualification,
        bank_account_no=request.bank_account_no,
        joining_date=request.joining_date,
        left_date=request.left_date
    )
    db.add(teacher_profile)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_accountant(db: Session, request: AccountantCreateRequest) -> User:
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise ValueError("A user with this email already exists.")

    new_user = User(
        email=request.email,
        name=request.name,
        hashed_password=hash_password(request.password),
        role="accountant",
        is_active=True,
        token_version=1
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    accountant_profile = AccountantProfile(
        user_id=new_user.id,
        base_salary=request.base_salary,
        qualification=request.qualification,
        bank_account_no=request.bank_account_no,
        joining_date=request.joining_date,
        left_date=request.left_date
    )
    db.add(accountant_profile)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_staff(db: Session, user_id: int, request: StaffUpdateRequest) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found.")

    if request.email and request.email != user.email:
        existing = db.query(User).filter(User.email == request.email).first()
        if existing:
            raise ValueError("Email already in use by another account.")
        user.email = request.email

    if request.name:
        user.name = request.name
    
    # Invalidate existing sessions if password is changed
    if request.password:
        user.hashed_password = hash_password(request.password)
        user.token_version = (user.token_version or 1) + 1

    if user.role == "teacher":
        if not user.teacher_profile:
            user.teacher_profile = TeacherProfile(user_id=user.id)
        user.teacher_profile.base_salary = request.base_salary
        user.teacher_profile.qualification = request.qualification
        user.teacher_profile.bank_account_no = request.bank_account_no
        user.teacher_profile.joining_date = request.joining_date
        user.teacher_profile.left_date = request.left_date

    elif user.role == "accountant":
        if not user.accountant_profile:
            user.accountant_profile = AccountantProfile(user_id=user.id)
        user.accountant_profile.base_salary = request.base_salary
        user.accountant_profile.qualification = request.qualification
        user.accountant_profile.bank_account_no = request.bank_account_no
        user.accountant_profile.joining_date = request.joining_date
        user.accountant_profile.left_date = request.left_date

    db.commit()
    db.refresh(user)
    return user

def get_all_users_by_role(db: Session, role: str):
    return db.query(User).filter(User.role == role).all()