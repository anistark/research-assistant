"""
Journal routes for the Research Assistant API
"""
from fastapi import APIRouter, HTTPException
from ..models import JournalResponse
from ..database import collection

router = APIRouter()

@router.get("/{journal_id}", response_model=JournalResponse)
async def get_journal(journal_id: str):
    """Get all chunks for a specific journal document"""
    try:
        results = collection.get(
            where={"source_doc_id": journal_id},
            include=["documents", "metadatas"]
        )
        
        if not results['ids']:
            raise HTTPException(status_code=404, detail="Journal not found")
        
        chunks = []
        for i in range(len(results['ids'])):
            chunks.append({
                "id": results['ids'][i],
                "text": results['documents'][i],
                "metadata": results['metadatas'][i]
            })
        
        return JournalResponse(
            journal_id=journal_id,
            chunks=chunks,
            total_chunks=len(chunks)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
