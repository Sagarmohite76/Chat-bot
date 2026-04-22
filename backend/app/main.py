from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import routes
from app.models.user import User,Chat
from app.db.base import Base
from app.db.database import engine

app=FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)
app.include_router(routes.router)