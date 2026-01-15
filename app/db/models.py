from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password_hash = Column(String)

    public_key = Column(LargeBinary)
    private_key = Column(LargeBinary)

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    filepath = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

class SharedKey(Base):
    __tablename__ = "shared_keys"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    recipient_id = Column(Integer, ForeignKey("users.id"))
    encrypted_aes_key = Column(LargeBinary)
