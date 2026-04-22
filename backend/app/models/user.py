from app.db.base import Base
from sqlalchemy import (
    Column, BigInteger, Text,ForeignKey,
    TIMESTAMP, func
)
from sqlalchemy.orm import relationship

# User table
class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    first_login = Column(TIMESTAMP, server_default=func.now())

# Chat table
class Chat(Base):
    __tablename__ = "chats"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(
        BigInteger,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )
    conversation_id = Column(BigInteger, nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


def get_query(db, user_id: int, query: str, conversation_id: int = None):
    
    if not query.strip():
        raise ValueError("Query cannot be empty")

    user = db.query(User).filter_by(user_id=user_id).first()
    if not user:
        user = User(user_id=user_id)
        db.add(user)
        db.commit()
        db.refresh(user)

    if not conversation_id:
        last_chat = db.query(Chat).order_by(Chat.id.desc()).first()
        conversation_id = (last_chat.conversation_id + 1) if last_chat else 1
    chat = Chat(
        user_id=user.user_id,
        conversation_id=conversation_id,
        message=query.strip()
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)

    return {
        "chat_id": chat.id,
        "user_id": chat.user_id,
        "conversation_id": chat.conversation_id,
        "message": chat.message
    }




