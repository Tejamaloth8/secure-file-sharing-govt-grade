from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import datetime
import os

# 🔐 LOAD SECRET FROM ENV (Render / Prod Safe)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable not set")

security = HTTPBearer(auto_error=True)

def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    payload["iat"] = datetime.datetime.utcnow()
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
