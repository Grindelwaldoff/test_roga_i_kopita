FROM python:3.11-slim AS base

ENV DB_URI=sqlite+aiosqlite:///./test.db

WORKDIR /app
COPY requirements.txt .
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .
COPY data ./data
COPY test.db .
RUN python3 -m pip install -r requirements.txt


EXPOSE 8000


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
