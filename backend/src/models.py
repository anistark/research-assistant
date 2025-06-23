"""
Pydantic models for the Research Assistant API
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ChunkData(BaseModel):
    id: str
    source_doc_id: str
    chunk_index: int
    section_heading: str
    doi: Optional[str] = None
    journal: str
    publish_year: int
    usage_count: int
    attributes: List[str]
    link: str
    text: str

class UploadRequest(BaseModel):
    chunks: List[ChunkData]
    schema_version: str = "1.0"

class SearchRequest(BaseModel):
    query: str
    k: int = 10
    min_score: float = 0.25

class SearchResult(BaseModel):
    id: str
    score: float
    text: str
    metadata: Dict[str, Any]

class UploadResponse(BaseModel):
    message: str
    schema_version: str

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total_found: int

class JournalResponse(BaseModel):
    journal_id: str
    chunks: List[Dict[str, Any]]
    total_chunks: int

class StatsResponse(BaseModel):
    total_chunks: int
    top_referenced_papers: List[Dict[str, Any]]
