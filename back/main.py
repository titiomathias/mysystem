from fastapi import FastAPI, Response, HTTPException, Depends
from routes import me, tasks
from schemas.models import UserLogin, UserRegister
from models.user import User
from models.attribute import Attribute
from db.session import engine
from db.base import Base
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.deps import get_db
from security.security import hash_password, verify_password
import models
from security.auth import generate_token

api = FastAPI()

@api.on_event("startup")
def startup():
    print("[#] Initializing database [#]")
    Base.metadata.create_all(bind=engine)


@api.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@api.post("/login")
async def login(userData: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(User.email == userData.email)
        .first()
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(userData.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = generate_token({"user_id": user.id, "email": user.email})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=1800
    )

    response.status_code = 200

    return {
        "message": "Login successful",
    }

@api.get("/logout")
async def logout():
    return {"message": "Logout successful"}


@api.post("/register")
async def register(user: UserRegister, response: Response, db: Session = Depends(get_db)):
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email or username already exists")
    
    new_attributes = Attribute(
        user_id=new_user.id,
        str=10,
        int=10,
        con=10,
        wis=10,
        cha=10,
        agi=10
    )

    try:
        db.add(new_attributes)
        db.commit()
        db.refresh(new_attributes)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create user attributes")

    token = generate_token({"user_id": new_user.id, "email": new_user.email})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=1800
    )

    response.status_code = 201

    return {
        "message": "registered successfully"
    }

api.include_router(me.router, prefix="/me", tags=["User"])
api.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])