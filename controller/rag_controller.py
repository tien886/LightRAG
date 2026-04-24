"""controller/rag_controller.py — FastAPI router for /api/rag/*.

No business logic here — only HTTP handling.
Business logic lives in service/rag/rag_service.py.
"""
from __future__ import annotations
from service.rag import get_rag_service

from fastapi import APIRouter, HTTPException
from dto import (
    RagQueryRequest,
    RagQueryResponse,
    RagIndexRequest,
    RagIndexResponse,
    RagSeedResponse,
)

router = APIRouter(prefix="/api/rag", tags=["rag"])


@router.post("/query", response_model=RagQueryResponse)
async def query_rag(request: RagQueryRequest) -> RagQueryResponse:
    """Query LightRAG directly with a specific mode."""
    return await get_rag_service().query(request)


@router.post("/index", response_model=RagIndexResponse)
async def index_documents(request: RagIndexRequest) -> RagIndexResponse:
    """Index raw text documents into LightRAG."""
    return await get_rag_service().index(request)


@router.delete("/doc/{doc_id}")
async def delete_document(doc_id: str) -> dict:
    """Delete a document and all its data from LightRAG."""
    return await get_rag_service().delete(doc_id)


@router.get("/status/{doc_id}")
async def get_document_status(doc_id: str) -> dict:
    """Get processing status of a document."""
    return await get_rag_service().get_status(doc_id)


@router.post("/seed", response_model=RagSeedResponse)
async def seed_academic_data() -> RagSeedResponse:
    """Seed initial academic documents into LightRAG. Admin only."""
    return await get_rag_service().seed_academic_data()