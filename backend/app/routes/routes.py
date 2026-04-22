from fastapi import APIRouter
from .schemas import ChatRequest, ChatResponse, IngestRequest, IngestResponse
from app.models.user import get_query
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.deps import get_db
from app.services.brain import response
import time
from app.embeddings.jina_embed import get_embedding
from app.vector_db.qdrant import add_data
from fastapi import File, UploadFile
import uuid
import json

router=APIRouter()

@router.get("/")
def get_users():
    return {"message":"users get successfully."}

@router.post("/query", response_model=ChatResponse)
def create_query(payload: ChatRequest, db: Session = Depends(get_db)):

    result = get_query(
        db=db,
        user_id=payload.user_id,
        query=payload.query,
        conversation_id=payload.conversation_id
    )

    answer, sources = response(payload.query)

    return ChatResponse(
        chat_id=result["chat_id"],              
        user_id=result["user_id"],
        conversation_id=result["conversation_id"],
        message=answer,
        sources=sources
    )

@router.post("/ingest", response_model=IngestResponse)
def ingest_data(payload: IngestRequest):
    unique_id = int(time.time() * 1000)
    
    vec = get_embedding(payload.text)
    
    add_data(unique_id, vec, {"text": payload.text})
    
    return IngestResponse(
        id=unique_id,
        message="Data successfully ingested into Qdrant."
    )

@router.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    # Read file content
    content = await file.read()
    filename = file.filename.lower()
    
    try:
        raw_text = content.decode("utf-8")
    except UnicodeDecodeError:
        return {"error": "Invalid file format. Please upload a UTF-8 encoded text or JSON file."}
    
    items_to_ingest = [] # List of (text_for_embedding, payload_dict)

    if filename.endswith(".json"):
        try:
            data = json.loads(raw_text)
            if not isinstance(data, list):
                return {"error": "JSON dataset must be a list of objects."}
            
            for item in data:
                if not isinstance(item, dict): continue
                
                # Construct text for embedding
                title = item.get("title", "")
                content_text = item.get("content", "")
                
                embedding_input = f"Title: {title}\nContent: {content_text}" if title else content_text
                
                if embedding_input.strip():
                    items_to_ingest.append((embedding_input, item))
                    
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format."}
    else:
        # Fallback to plain text paragraph splitting
        chunks = [chunk.strip() for chunk in raw_text.split("\n\n") if chunk.strip()]
        if not chunks:
            chunks = [line.strip() for line in raw_text.split("\n") if line.strip()]
        
        for chunk in chunks:
            items_to_ingest.append((chunk, {"text": chunk}))

    ingested_count = 0
    for text_to_embed, payload in items_to_ingest:
        unique_id = int(time.time() * 1000) + ingested_count
        try:
            vec = get_embedding(text_to_embed)
            add_data(unique_id, vec, payload)
            ingested_count += 1
        except Exception as e:
            print(f"Failed to ingest item: {e}")
            pass

    return {
        "message": f"Successfully ingested {ingested_count} items from {file.filename}."
    }