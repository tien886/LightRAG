"""Configuration for LightRAG + Neo4j + Gemini + SiliconCloud.

Only two providers are used:
  • LLM      — Gemini Pro  (via Anthropic-compatible /vertexai endpoint)
  • Embedding — SiliconCloud (BAAI/bge-m3, OpenAI-compatible)
"""
from __future__ import annotations
import os
from dotenv import load_dotenv

load_dotenv()


NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME: str = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "password")

GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
GEMINI_BASE_URL: str = os.getenv(
    "GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/vertexai/version"
)
GEMINI_MODEL_NAME: str = os.getenv("GEMINI_MODEL_NAME", "gemini-2.0-flash")
GEMINI_ANTHROPIC_BASE_URL: str = os.getenv("GEMINI_ANTHROPIC_BASE_URL", "")

SILICONCLOUD_API_KEY: str = os.getenv("SILICONCLOUD_API_KEY", "")
SILICONCLOUD_BASE_URL: str = os.getenv(
    "SILICONCLOUD_BASE_URL", "https://api.siliconcloud.cn/v1"
)
SILICONCLOUD_EMBEDDING_MODEL: str = os.getenv(
    "SILICONCLOUD_EMBEDDING_MODEL", "BAAI/bge-m3"
)

RAG_WORKING_DIR: str = os.getenv("RAG_WORKING_DIR", "./rag_working")

CHUNK_TOKEN_SIZE: int = int(os.getenv("CHUNK_TOKEN_SIZE", "1024"))
CHUNK_OVERLAP_TOKEN_SIZE: int = int(os.getenv("CHUNK_OVERLAP_TOKEN_SIZE", "100"))
