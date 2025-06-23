"""
Statistics routes for the Research Assistant API
"""
from fastapi import APIRouter, HTTPException
from ..models import StatsResponse
from ..database import collection

router = APIRouter()

@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get system statistics"""
    try:
        collection_count = collection.count()

        all_results = collection.get(include=["metadatas"])
        usage_stats = {}
        
        for metadata in all_results['metadatas']:
            doc_id = metadata['source_doc_id']
            usage_count = metadata.get('usage_count', 0)
            
            if doc_id not in usage_stats:
                usage_stats[doc_id] = {
                    'journal': metadata.get('journal', 'Unknown'),
                    'total_usage': 0
                }
            usage_stats[doc_id]['total_usage'] += usage_count

        top_papers = sorted(
            usage_stats.items(), 
            key=lambda x: x[1]['total_usage'], 
            reverse=True
        )[:10]
        
        return StatsResponse(
            total_chunks=collection_count,
            top_referenced_papers=[
                {
                    "source_doc_id": doc_id,
                    "journal": stats['journal'],
                    "total_usage": stats['total_usage']
                }
                for doc_id, stats in top_papers
            ]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
