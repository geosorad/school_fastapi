from sqlalchemy import Column, String
from app.core.database import Base

class Student(Base):
    __tablename__ = "students"

    regd = Column(String, primary_key=True, index=True, nullable=False) # PK
    roll_no = Column(String, nullable=True)
    name = Column(String, nullable=False) # Required
    class_name = Column(String, nullable=True) # (class is a SQL reserved keyword)
    dob = Column(String, nullable=True) # BS date
    address = Column(String, nullable=True)
    contact_no = Column(String, nullable=True)