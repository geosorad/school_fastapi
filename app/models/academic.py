from sqlalchemy import Column, String, Float, Integer, ForeignKey
from app.core.database import Base

class Topic(Base):
    __tablename__ = "topics"

    id = Column(String, primary_key=True, index=True) # UUID/client-generated string
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    class_name = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(String, nullable=False) # ISO or YYYY-MM-DD string


class StudentAssessment(Base):
    __tablename__ = "student_assessments"

    id = Column(String, primary_key=True, index=True) # {student_regd}_{topic_id}_{criterion}_{date}
    topic_id = Column(String, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    student_regd = Column(String, ForeignKey("students.regd", ondelete="CASCADE"), nullable=False)
    criterion = Column(String, nullable=False) # HW, Writing, Presentation, Reading, Meaning, Content
    rating = Column(Float, nullable=False, default=0.0)
    assessment_date = Column(String, nullable=False) # YYYY-MM-DD
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    updated_at = Column(String, nullable=False)