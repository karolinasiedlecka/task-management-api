from fastapi import FastAPI
from app.routers import tasks
from app.database import engine, Base
from app import models_db

app = FastAPI(
    title="Task Management API",
    description="A REST API for managing tasks.",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)

app.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["Tasks"]
)


@app.get("/")
def read_root():
    return {"message": "Welcome to Task Management API"}