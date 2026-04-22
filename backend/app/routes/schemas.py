from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    user_id: int
    query: str
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    chat_id: int
    user_id: int
    conversation_id: int
    message: str
    sources: Optional[str] = None

class IngestRequest(BaseModel):
    text: str

class IngestResponse(BaseModel):
    id: int
    message: str