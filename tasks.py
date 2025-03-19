from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Task
from schemas import TaskCreate, TaskUpdate

task_router = APIRouter()

@task_router.post("/")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(**task.dict())
    db.add(new_task)
    db.commit()
    return {"message": "Task created"}

@task_router.get("/")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@task_router.put("/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = task_update.status
    db.commit()
    return {"message": "Task updated"}

@task_router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}
