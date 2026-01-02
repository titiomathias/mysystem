from fastapi import Cookie, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
TOKEN_EXPIRE_HOURS = int(os.environ.get("TOKEN_EXPIRE_HOURS"))

def generate_token(payload: dict):
    dados = payload.copy()
    dados["exp"] = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(access_token: str = Cookie(None)):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    

async def verify_cookie(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(401, "Token ausente")

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(401, "Token inválido ou expirado")