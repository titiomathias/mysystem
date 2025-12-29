from fastapi import APIRouter

router = APIRouter()

# Get all tasks
@router.get("/")
async def get_tasks():
    return {"tasks": ["task1", "task2", "task3"]}


# Create a new task
@router.post("/")
async def create_task(task: dict):
    return {"task": task}


# Delete a task
@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    return {"message": f"Task {task_id} deleted"}


# Update a task
@router.put("/tasks/{task_id}")
async def update_task(task_id: int, task: dict):
    return {"task_id": task_id, "updated_task": task}


# Mark a task as complete
@router.post("/tasks/{task_id}/complete")
async def complete_task(task_id: int):
    return {"message": f"Task {task_id} completed"}
