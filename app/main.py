from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.routes import auth, users, students, configs, academics
from app.services.user_service import seed_default_admin

def run_database_migrations():
    db = SessionLocal()
    try:
        migration_statements = [
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS token_version INTEGER DEFAULT 1;",
            "ALTER TABLE teacher_profiles ADD COLUMN IF NOT EXISTS left_date VARCHAR;",
            "ALTER TABLE accountant_profiles ADD COLUMN IF NOT EXISTS left_date VARCHAR;",
            "CREATE TABLE IF NOT EXISTS students (regd VARCHAR PRIMARY KEY, roll_no VARCHAR, name VARCHAR NOT NULL, class_name VARCHAR, dob VARCHAR, address VARCHAR, contact_no VARCHAR);",
            "CREATE TABLE IF NOT EXISTS daily_schedules (id SERIAL PRIMARY KEY, class_name VARCHAR NOT NULL, period INTEGER NOT NULL, subject VARCHAR NOT NULL, teacher_id INTEGER REFERENCES users(id) ON DELETE SET NULL);",
            "CREATE TABLE IF NOT EXISTS fee_configs (class_name VARCHAR PRIMARY KEY, monthly_fee REAL DEFAULT 0.0, admission_fee REAL DEFAULT 0.0);",
            
            # Academic models
            """CREATE TABLE IF NOT EXISTS topics (
                id VARCHAR PRIMARY KEY,
                teacher_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                class_name VARCHAR NOT NULL,
                subject VARCHAR NOT NULL,
                title VARCHAR NOT NULL,
                description VARCHAR,
                created_at VARCHAR NOT NULL
            );""",
            """CREATE TABLE IF NOT EXISTS student_assessments (
                id VARCHAR PRIMARY KEY,
                topic_id VARCHAR REFERENCES topics(id) ON DELETE CASCADE,
                student_regd VARCHAR REFERENCES students(regd) ON DELETE CASCADE,
                criterion VARCHAR NOT NULL,
                rating REAL NOT NULL DEFAULT 0.0,
                assessment_date VARCHAR NOT NULL,
                teacher_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                updated_at VARCHAR NOT NULL
            );"""
        ]
        
        for statement in migration_statements:
            try:
                db.execute(text(statement))
                db.commit()
            except Exception as stmt_err:
                db.rollback()
                print(f"Migration notice: {stmt_err}")
    except Exception as e:
        print(f"Migration error: {e}")
    finally:
        db.close()

run_database_migrations()
Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    seed_default_admin(db)
finally:
    db.close()

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(students.router)
app.include_router(configs.router)
app.include_router(academics.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Sorad School Accounts API!"}