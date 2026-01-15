from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.deps import get_db
from app.db.models import User
from app.core.security import hash_password, verify_password
from app.services.crypto_service import generate_keypair
from app.core.auth import create_access_token

router = APIRouter()

class Auth(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(data: Auth, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Exists")

    priv, pub = generate_keypair()
    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        private_key=priv,
        public_key=pub
    )
    db.add(user)
    db.commit()
    return {"message": "Registered"}

@router.post("/login")
def login(data: Auth, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    return {"access_token": create_access_token({"sub": user.email})}
