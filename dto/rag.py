"""dto/rag.py — FastAPI request/response models for RAG endpoints."""
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Literal, Optional


class ChatRequest(BaseModel):
    question: str
    authentication: str = Field(description="Bearer token or raw JWT for authentication")


class ChatResponse(BaseModel):
    answer: str



class RagQueryRequest(BaseModel):
    question: str
    mode: Literal["naive", "local", "global", "hybrid", "mix"] = "naive"
    top_k: int = 60
    response_type: str = "Multiple Paragraphs"
    only_need_context: bool = False


class RagQueryResponse(BaseModel):
    answer: str
    mode: str



class RagIndexRequest(BaseModel):
    documents: list[str]
    source: str = "manual"


class RagIndexResponse(BaseModel):
    indexed_count: int
    document_ids: list[str]



class RagSeedResponse(BaseModel):
    indexed_count: int
    document_ids: list[str]
    sources: list[str]
