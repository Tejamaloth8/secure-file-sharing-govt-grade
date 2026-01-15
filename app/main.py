from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.api.auth import router as auth_router
from app.api.files import router as file_router
from app.api.share import router as share_router

app = FastAPI(title="Govt Grade Secure File Sharing")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(file_router)
app.include_router(share_router)

Base.metadata.create_all(bind=engine)
