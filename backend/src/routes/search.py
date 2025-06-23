"""
Search routes for the Research Assistant API
"""
from fastapi import APIRouter, HTTPException
from ..models import SearchRequest, SearchResponse, SearchResult
from ..database import collection
from ..embeddings import generate_embedding

router = APIRouter()

@router.post("/similarity_search", response_model=SearchResponse)
async def similarity_search(request: SearchRequest):
    """Perform semantic similarity search"""
    try:
        query_embedding = generate_embedding(request.query)

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=request.k,
            include=["documents", "metadatas", "distances"]
        )

        search_results = []
        for i in range(len(results['ids'][0])):
            score = 1 - results['distances'][0][i]
            
            if score >= request.min_score:
                chunk_id = results['ids'][0][i]
                metadata = results['metadatas'][0][i]
                current_usage = metadata.get('usage_count', 0)
                
                collection.update(
                    ids=[chunk_id],
                    metadatas=[{**metadata, 'usage_count': current_usage + 1}]
                )
                
                search_results.append(SearchResult(
                    id=chunk_id,
                    score=score,
                    text=results['documents'][0][i],
                    metadata=metadata
                ))
        
        return SearchResponse(
            query=request.query,
            results=search_results,
            total_found=len(search_results)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
