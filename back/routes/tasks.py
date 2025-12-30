from fastapi import APIRouter, HTTPException, Depends
from models.task import Task, TaskAttribute
from schemas.models import TaskModel
from security.auth import verify_cookie
from db.deps import get_db

router = APIRouter()

# Get all tasks
@router.get("/")
def get_tasks(user = Depends(verify_cookie), db = Depends(get_db)):
    tasks = db.query(Task).filter(Task.user_id == user["user_id"]).all()

    return {
        "tasks": tasks
    }


# Create a new task
@router.post("/")
def create_task(task: TaskModel, task_attribute: TaskAttribute, user = Depends(verify_cookie), db = Depends(get_db)):
    task.user_id = user["user_id"]

    # Save task


# Delete a task
@router.delete("/{task_id}")
def delete_task(task_id: int, user = Depends(verify_cookie), db = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user["user_id"]).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": f"Task deleted"}


# Update a task
@router.put("/{task_id}")
def update_task(task_id: int, task: Task, user = Depends(verify_cookie), db = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == user["user_id"]).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update fields

# Mark a task as complete
@router.post("/{task_id}/complete")
def complete_task(task_id: int):
    return {"message": f"Task {task_id} completed"}
