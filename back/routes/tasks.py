from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy import func
from models.task import Task
from models.user import User
from models.task_log import TaskLog
from models.task_attribute import TaskAttribute
from schemas.models import TaskOut, TaskStatus, TaskCreate, TaskUpdate
from security.auth import verify_cookie
from db.deps import get_db
from core.progression import xp_to_next_level, can_complete_task
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Query

router = APIRouter()

# Get all tasks
@router.get("", response_model=list[TaskOut])
def get_tasks(
    user=Depends(verify_cookie),
    db: Session = Depends(get_db),

    can_complete: Optional[bool] = Query(None),
    xp: Optional[str] = Query(None),
    attribute: Optional[str] = Query(None),
):
    
    query = (
        db.query(Task)
        .options(joinedload(Task.attributes))
        .filter(Task.user_id == user["user_id"])
    )

    if xp == "high":
        query = query.order_by(Task.base_xp.desc())

    if attribute:
        query = query.join(Task.attributes).filter(
            TaskAttribute.attribute == attribute
        )

    tasks = (
        query
        .order_by(
            Task.frequency.desc(),
            Task.last_completed_at.asc().nullsfirst()
        )
        .all()
    )

    result: list[TaskOut] = []

    for task in tasks:
        task_can_complete = can_complete_task(task)

        if can_complete is not None and task_can_complete != can_complete:
            continue

        result.append(
            TaskOut(
                id=task.id,
                name=task.name,
                description=task.description,
                category=task.category,
                frequency=task.frequency,
                base_xp=task.base_xp,
                status=task.status,
                last_completed_at=task.last_completed_at,
                streak_count=task.streak_count,
                best_streak=task.best_streak,
                can_complete=task_can_complete,
                is_completed_today=not task_can_complete,
                attributes=task.attributes
            )
        )

    return result


@router.post("/new-task", response_model=TaskOut, status_code=201)
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
        status=TaskStatus.PENDING,
        streak_count=0,
        best_streak=0,
        last_completed_at=None
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

    task.can_complete = can_complete_task(task)
    task.is_completed_today = not task.can_complete

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

    # 🔥 MESMA LÓGICA DO GET
    can_complete = can_complete_task(db_task)

    return TaskOut(
        id=db_task.id,
        name=db_task.name,
        description=db_task.description,
        category=db_task.category,
        frequency=db_task.frequency,
        base_xp=db_task.base_xp,
        status=db_task.status,
        last_completed_at=db_task.last_completed_at,
        streak_count=db_task.streak_count,
        best_streak=db_task.best_streak,
        attributes=db_task.attributes,

        can_complete=can_complete,
        is_completed_today=not can_complete
    )


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

    now = datetime.utcnow()

    # 2. Validação de repetição
    if task.last_completed_at:
        if task.frequency == "once":
            raise HTTPException(status_code=400, detail="Task already completed")

        if task.frequency == "daily":
            if task.last_completed_at.date() == now.date():
                raise HTTPException(status_code=400, detail="Task already completed today")

        if task.frequency == "weekly":
            if task.last_completed_at >= now - timedelta(days=7):
                raise HTTPException(status_code=400, detail="Task already completed this week")

    # 3. Atualiza streak
    if task.last_completed_at:
        delta = now.date() - task.last_completed_at.date()

        if task.frequency == "daily" and delta.days == 1:
            task.streak_count += 1
        elif task.frequency == "weekly" and delta.days <= 7:
            task.streak_count += 1
        else:
            task.streak_count = 1
    else:
        task.streak_count = 1

    task.best_streak = max(task.best_streak, task.streak_count)

    # 4. Calcula XP
    attr_bonus = sum(a.value for a in task.attributes)
    streak_bonus = int(task.base_xp * min(task.streak_count * 0.05, 0.5))
    xp_earned = task.base_xp + attr_bonus + streak_bonus

    # 5. Atualiza task
    task.last_completed_at = now

    if task.frequency == "once":
        task.status = TaskStatus.DONE

    # 6. Log
    db.add(
        TaskLog(
            task_id=task.id,
            user_id=user["user_id"],
            xp_earned=xp_earned,
            streak_at_completion=task.streak_count
        )
    )

    # 7. Level up (derivado dos logs)
    total_xp = (
        db.query(func.sum(TaskLog.xp_earned))
        .filter(TaskLog.user_id == user["user_id"])
        .scalar()
    ) or 0

    db_user = db.query(User).filter(User.id == user["user_id"]).first()

    while total_xp >= xp_to_next_level(db_user.level):
        total_xp -= xp_to_next_level(db_user.level)
        db_user.level += 1

        db_user.attributes.str += 1
        db_user.attributes.agi += 1
        db_user.attributes.int += 1
        db_user.attributes.con += 1
        db_user.attributes.wis += 1
        db_user.attributes.cha += 1

    db_user = db.query(User).filter(User.id == user["user_id"]).first()

    for attr in task.attributes:
        if attr.attribute == "str":
            db_user.attributes.str += attr.value
        elif attr.attribute == "agi":
            db_user.attributes.agi += attr.value
        elif attr.attribute == "int":
            db_user.attributes.int += attr.value
        elif attr.attribute == "con":
            db_user.attributes.con += attr.value
        elif attr.attribute == "wis":
            db_user.attributes.wis += attr.value
        elif attr.attribute == "cha":
            db_user.attributes.cha += attr.value

    db.commit()

    return {
        "message": "Task completed",
        "xp_earned": xp_earned,
        "streak": task.streak_count,
        "level": db_user.level
    }
