from qdrant_client import QdrantClient
from app.core.config import setting
from qdrant_client.models import VectorParams, Distance
 
client = QdrantClient(
    url=setting.QDRANT_URL,
    api_key=setting.QDRANT_API_KEY
)
 
if setting.QDRANT_COLLECTION not in [c.name for c in client.get_collections().collections]:
    client.create_collection(
        collection_name=setting.QDRANT_COLLECTION,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )
 
 
 
def add_data(ids:int, vec:list, payload:dict):
    client.upsert(
        collection_name=setting.QDRANT_COLLECTION,
        points=[
            {
                "id": ids,
                "vector": vec,
                "payload": payload
            }
        ]
    )
   
 
 
def retrive_data(vec):
    points = client.query_points(
        collection_name=setting.QDRANT_COLLECTION,
        query=vec,
        limit=6,
        with_payload=True
    )
 
    return points
 
 
 