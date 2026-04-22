from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import setting

engine=create_engine(setting.DATABASE_URL,echo=True)

SessionLocal=sessionmaker(
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)