from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Simple Task Manager")

app.include_router(tasks.router)


@app.get("/")
def root():
    return {"status": "Task Manager is running"}
