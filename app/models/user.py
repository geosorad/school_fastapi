from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'admin', 'teacher', 'accountant'
    is_active = Column(Boolean, default=True)
    token_version = Column(Integer, default=1, nullable=False)

    teacher_profile = relationship("TeacherProfile", uselist=False, back_populates="user", cascade="all, delete-orphan")
    accountant_profile = relationship("AccountantProfile", uselist=False, back_populates="user", cascade="all, delete-orphan")


class TeacherProfile(Base):
    __tablename__ = "teacher_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    base_salary = Column(Float, nullable=True)
    qualification = Column(String, nullable=True)
    bank_account_no = Column(String, nullable=True)
    joining_date = Column(String, nullable=True)
    left_date = Column(String, nullable=True)

    user = relationship("User", back_populates="teacher_profile")


class AccountantProfile(Base):
    __tablename__ = "accountant_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    base_salary = Column(Float, nullable=True)
    qualification = Column(String, nullable=True)
    bank_account_no = Column(String, nullable=True)
    joining_date = Column(String, nullable=True)
    left_date = Column(String, nullable=True)

    user = relationship("User", back_populates="accountant_profile")


class DailySchedule(Base):
    __tablename__ = "daily_schedules"

    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String, nullable=False)
    period = Column(Integer, nullable=False)
    subject = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)


class FeeConfig(Base):
    __tablename__ = "fee_configs"

    class_name = Column(String, primary_key=True, index=True, nullable=False)
    monthly_fee = Column(Float, default=0.0)
    admission_fee = Column(Float, default=0.0)