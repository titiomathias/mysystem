from fastapi import FastAPI, include_router
from routes import me, tasks
from models.models import UserLogin, UserRegister

api = FastAPI()

@api.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@api.post("/login")
async def login():
    return {"message": "Login successful"}


@api.get("/logout")
async def logout():
    return {"message": "Logout successful"}


@api.post("/register")
async def register():
    return {"message": "Registration successful"}


api.include_router(me.router, prefix="/me", tags=["User"])
api.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])