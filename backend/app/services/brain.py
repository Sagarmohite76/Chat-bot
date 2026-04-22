from app.embeddings.jina_embed import get_embedding
from app.vector_db.qdrant import retrive_data
from app.llm.generator import get_response

def response(query):
    vector = get_embedding(query)
    results = retrive_data(vector)
    
    # Step 1: Robustly extract points from various possible response structures
    if hasattr(results, 'points'):
        # For recent query_points() responses
        points = results.points
    elif isinstance(results, list):
        points = results
    elif isinstance(results, tuple) and results:
        # Handling possible double-tuple from older patterns
        points = results[0] if isinstance(results[0], (list, tuple)) else results
    else:
        points = []

    # Step 2: Extract context chunks from payloads
    context_chunks = []
    for p in points:
        # Handle if p is a tuple (older pattern)
        point_obj = p[0] if isinstance(p, tuple) else p
        
        payload = getattr(point_obj, "payload", {})
        if payload:
            text = payload.get("text")
            content = payload.get("content")
            title = payload.get("title")
            
            chunk = ""
            if text:
                chunk = text
            elif content:
                # Format structured JSON content nicely
                chunk = f"Title: {title}\n{content}" if title else content
            
            if chunk:
                context_chunks.append(chunk)

    context = "\n\n".join(context_chunks) or "No relevant information found."
    answer = get_response(query, context)

    return answer, context