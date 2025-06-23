"""
Upload routes for the Research Assistant API
"""
import json
from fastapi import APIRouter, HTTPException
from ..models import UploadRequest, UploadResponse
from ..database import collection
from ..embeddings import generate_embedding

router = APIRouter()

@router.put("/upload", status_code=202, response_model=UploadResponse)
async def upload_chunks(request: UploadRequest):
    """Upload and embed journal chunks"""
    try:
        chunk_count = len(request.chunks)
        
        for chunk in request.chunks:
            embedding = generate_embedding(chunk.text)
            
            metadata = {
                "source_doc_id": chunk.source_doc_id,
                "chunk_index": chunk.chunk_index,
                "section_heading": chunk.section_heading,
                "doi": chunk.doi or "",
                "journal": chunk.journal,
                "publish_year": chunk.publish_year,
                "usage_count": chunk.usage_count,
                "attributes": json.dumps(chunk.attributes),
                "link": chunk.link
            }
            
            collection.add(
                ids=[chunk.id],
                embeddings=[embedding],
                documents=[chunk.text],
                metadatas=[metadata]
            )
        
        return UploadResponse(
            message=f"Successfully uploaded {chunk_count} chunks",
            schema_version=request.schema_version
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
