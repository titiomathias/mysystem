from fastapi import FastAPI, Response, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
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
from security.auth import generate_token
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


api = FastAPI(
    title="MySystem API",
    description="API para o sistema de gamificação de tarefas MySystem",
    version="1.0.0",
    docs_url=None
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mysystem.discloud.app",
        "https://0.0.0.0:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.mount("/app", StaticFiles(directory="static", html=True), name="static")

@api.on_event("startup")
def startup():
    print("[#] Initializing database [#]")
    Base.metadata.create_all(bind=engine)


@api.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/app/index.html")


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
        samesite="none",
        secure=True,
        path="/",
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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:api",
        host="0.0.0.0",
        port=8080,
        log_level="info",
        workers=1
    )
