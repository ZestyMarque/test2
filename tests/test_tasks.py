from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base, get_db
from main import app


# тестовая база данных
TEST_DB_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DB_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)


# подмена зависимости для базы данных
def test_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = test_get_db

client = TestClient(app)


def test_create_task():
    resp = client.post("/tasks/", json={
        "title": "First test task",
        "description": "task from test"
    })

    assert resp.status_code == 200

    data = resp.json()
    assert data["title"] == "First test task"
    assert data["completed"] == False


def test_get_tasks():
    resp = client.get("/tasks/")
    assert resp.status_code == 200

    tasks = resp.json()
    assert type(tasks) == list


def test_get_one_task():
    resp = client.get("/tasks/1")
    assert resp.status_code == 200

    task = resp.json()
    assert task["id"] == 1


def test_finish_task():
    resp = client.put("/tasks/1")
    assert resp.status_code == 200

    task = resp.json()
    assert task["completed"] == True


def test_remove_task():
    resp = client.delete("/tasks/1")
    assert resp.status_code == 200

    result = resp.json()
    assert result["message"] == "Task deleted"
