from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.models import Task, TaskCreate
from app.models_db import TaskDB
from app.database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[Task])
def get_tasks(status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(TaskDB)

    if status:
        query = query.filter(TaskDB.status == status)

    return query.all()


@router.post("", response_model=Task, status_code=201)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    new_task = TaskDB(**task_data.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_data.model_dump().items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully", "task_id": task_id}