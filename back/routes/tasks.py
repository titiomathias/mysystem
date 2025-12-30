from fastapi import APIRouter, HTTPException, Depends, Response
from models.task import Task
from models.user import User
from models.task_log import TaskLog
from models.task_attribute import TaskAttribute
from schemas.models import TaskOut, TaskStatus, TaskCreate, TaskUpdate
from security.auth import verify_cookie
from db.deps import get_db
from core.progression import xp_to_next_level
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

router = APIRouter()

# Get all tasks
@router.get("/")
def get_tasks(user = Depends(verify_cookie), db = Depends(get_db)):
    tasks = db.query(Task).filter(Task.user_id == user["user_id"]).all()

    return {
        "tasks": tasks
    }


@router.post("/", response_model=TaskOut, status_code=201)
def create_task(
    task_data: TaskCreate,
    user=Depends(verify_cookie),
    db: Session = Depends(get_db)
):
    task = Task(
        name=task_data.name,
        description=task_data.description,
        category=task_data.category,
        frequency=task_data.frequency,
        base_xp=task_data.base_xp,
        user_id=user["user_id"],
        status=TaskStatus.PENDING
    )

    db.add(task)
    db.flush()

    for attr in task_data.attributes:
        db.add(
            TaskAttribute(
                task_id=task.id,
                attribute=attr.attribute.value,
                value=attr.value
            )
        )

    db.commit()
    db.refresh(task)

    return task


# Delete a task
@router.delete("/{task_id}")
def delete_task(task_id: int, user = Depends(verify_cookie), db = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user["user_id"]).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": f"Task deleted"}


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user=Depends(verify_cookie),
    db: Session = Depends(get_db)
):
    db_task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == user["user_id"])
        .first()
    )

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in task_data.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)

    return db_task


@router.post("/{task_id}/complete")
def complete_task(
    task_id: int,
    user=Depends(verify_cookie),
    db: Session = Depends(get_db)
):
    # 1. Busca task
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == user["user_id"])
        .first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # 2. Validação de repetição
    last_log = (
        db.query(TaskLog)
        .filter(
            TaskLog.task_id == task.id,
            TaskLog.user_id == user["user_id"]
        )
        .order_by(TaskLog.completed_at.desc())
        .first()
    )

    now = datetime.utcnow()

    if task.frequency == "once" and last_log:
        raise HTTPException(status_code=400, detail="Task already completed")

    if task.frequency == "daily" and last_log:
        if last_log.completed_at.date() == now.date():
            raise HTTPException(status_code=400, detail="Task already completed today")

    if task.frequency == "weekly" and last_log:
        if last_log.completed_at >= now - timedelta(days=7):
            raise HTTPException(status_code=400, detail="Task already completed this week")

    # 3. Calcula XP
    attr_bonus = sum(a.value for a in task.attributes)
    xp_earned = task.base_xp + attr_bonus

    # 4. Atualiza usuário
    db_user = db.query(User).filter(User.id == user["user_id"]).first()

    db_user.xp += xp_earned

    # 5. Level up
    while db_user.xp >= xp_to_next_level(db_user.level):
        db_user.xp -= xp_to_next_level(db_user.level)
        db_user.level += 1

        # ganha +1 em todos atributos
        db_user.attributes.str += 1
        db_user.attributes.agi += 1
        db_user.attributes.int += 1
        db_user.attributes.con += 1
        db_user.attributes.wis += 1
        db_user.attributes.cha += 1

    # 6. Log
    db.add(
        TaskLog(
            task_id=task.id,
            user_id=db_user.id,
            xp_earned=xp_earned
        )
    )

    # 7. Status
    if task.frequency == "once":
        task.status = TaskStatus.DONE

    db.commit()

    return {
        "message": "Task completed",
        "xp_earned": xp_earned,
        "level": db_user.level
    }

