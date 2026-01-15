from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.deps import get_db
from app.db.models import User, SharedKey
from app.core.auth import get_current_user
from app.services.key_exchange import *

router = APIRouter()

class Share(BaseModel):
    recipient_email: str
    document_id: int

@router.post("/share")
def share(data: Share, email=Depends(get_current_user), db: Session = Depends(get_db)):
    owner = db.query(User).filter(User.email == email).first()
    recipient = db.query(User).filter(User.email == data.recipient_email).first()

    owner_key = db.query(SharedKey).filter_by(
        document_id=data.document_id,
        recipient_id=owner.id
    ).first()

    aes = decrypt_aes_key(owner.private_key, owner_key.encrypted_aes_key)

    db.add(SharedKey(
        document_id=data.document_id,
        recipient_id=recipient.id,
        encrypted_aes_key=encrypt_aes_key(recipient.public_key, aes)
    ))
    db.commit()

    return {"message": "Shared securely"}
