from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "chave-super-secreta-para-treinamento"
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 1

def generate_token(payload: dict):
    dados = payload.copy()
    dados["exp"] = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None