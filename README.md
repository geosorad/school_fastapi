# Welcome to your Fastapi Server 👋

#neon

This is an Fastapi project created with `python`

## 1. Create virtual env

```bash
python -m venv venv
```

## 2. Activate venv

```bash
source venv/bin/activate
```

## 3. Install basics

```bash
pip install fastapi uvicorn
```

## 4. Main.py

```python
from fastapi import FastAPI

app = FastAPI(title="School Management API")


@app.get("/")
def root():
    return {
        "message": "School API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }
```

## 5. Run project

```bash
uvicorn app.main:app --reload
```

### OR

```bash
uvicorn app.main:app --host 0.0.0.0 --reload
```

## 6. Testing

```url
http://127.0.0.1:8000/docs
```

## 7. Neon postgress

```bash
pip install sqlalchemy psycopg2-binary "pydantic[email]" python-dotenv
```

### requirements.txt

```bash
pip freeze > requirements.txt
```

pip install -r requirements.txt