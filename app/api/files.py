from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import uuid, os, tempfile

from app.db.deps import get_db
from app.db.models import User, Document, SharedKey
from app.core.auth import get_current_user
from app.services.file_crypto import *
from app.services.key_exchange import *

router = APIRouter()

@router.post("/upload")
def upload(file: UploadFile = File(...),
           email=Depends(get_current_user),
           db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()
    aes = generate_aes_key()
    enc = encrypt_file(file.file.read(), aes)

    path = f"storage/{uuid.uuid4()}_{file.filename}"
    open(path, "wb").write(enc)

    doc = Document(filename=file.filename, filepath=path, owner_id=user.id)
    db.add(doc); db.commit(); db.refresh(doc)

    db.add(SharedKey(
        document_id=doc.id,
        recipient_id=user.id,
        encrypted_aes_key=encrypt_aes_key(user.public_key, aes)
    ))
    db.commit()

    return {"document_id": doc.id}

@router.get("/download/{doc_id}")
def download(doc_id: int,
             email=Depends(get_current_user),
             db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()
    key = db.query(SharedKey).filter_by(document_id=doc_id, recipient_id=user.id).first()
    doc = db.query(Document).filter_by(id=doc_id).first()

    aes = decrypt_aes_key(user.private_key, key.encrypted_aes_key)
    data = decrypt_file(open(doc.filepath, "rb").read(), aes)

    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(data); tmp.close()
    return {"file": tmp.name}
