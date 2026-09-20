from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

db_url = settings.DATABASE_URL
# Ensure SQLAlchemy-compatible dialect prefix is present
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# Connect to database
engine = create_engine(
    db_url, 
    pool_pre_ping=True,  # Keeps connections alive/re-establishes broken links
    pool_recycle=3600    # Prevents server-side timeout issues on Neon
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()