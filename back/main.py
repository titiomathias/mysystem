from fastapi import FastAPI

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


