from fastapi import Router

router = Router()

@router.get("/tasks")
async def get_tasks():
    return {"tasks": ["task1", "task2", "task3"]}