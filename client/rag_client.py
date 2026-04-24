"""client/rag_client.py — Gemini LLM + SiliconCloud embedding (pure httpx, no SDK).

  • LLM   — Gemini native REST API (google-generativelanguage.googleapis.com)
  • Embed — SiliconCloud REST API (api.siliconflow.com)

Usage:
    from client.rag_client import get_llm_func, get_embedding_func
"""
from __future__ import annotations

import os
import httpx
import numpy as np
from dotenv import load_dotenv

load_dotenv()

from lightrag.utils import EmbeddingFunc


def get_llm_func() -> callable:
    """
    Async Gemini LLM function for LightRAG.
    Uses Google Generative Language REST API.
    """

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    model = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash").strip()
    base_url = os.getenv(
        "GEMINI_BASE_URL",
        "https://generativelanguage.googleapis.com/v1beta"
    ).strip()

    async def llm_func(
        prompt: str,
        system_prompt: str = "",
        history: list[dict] | None = None,
        **kwargs,
    ) -> str:

        max_tokens = int(kwargs.get("max_tokens", 1024))
        temperature = float(kwargs.get("temperature", 0.0))

        contents: list[dict] = []

        if history:
            for msg in history:
                contents.append({
                    "role": "model" if msg.get("role") == "assistant" else "user",
                    "parts": [{"text": str(msg.get("content", ""))}],
                })

        contents.append({
            "role": "user",
            "parts": [{"text": str(prompt)}],
        })

        payload = {
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature,
            },
        }

        if system_prompt:
            payload["systemInstruction"] = {
                "parts": [{"text": system_prompt}]
            }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{base_url}/models/{model}:generateContent",
                params={"key": api_key},
                json=payload,
            )

            if response.status_code >= 400:
                raise RuntimeError(
                    f"Gemini API error {response.status_code}: {response.text}"
                )

            data = response.json()

        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            raise RuntimeError(f"Unexpected Gemini response: {data}")

    return llm_func


_EMBEDDING_DIM = 4096


def get_embedding_func() -> EmbeddingFunc:
    """Async SiliconCloud embedding function wrapped in EmbeddingFunc.
    LightRAG's EmbeddingFunc expects exactly 1 output vector per input text.
    The inner function returns np.ndarray so EmbeddingFunc.size works.
    """
    api_key = os.getenv("SILICONCLOUD_API_KEY", "")
    base_url = os.getenv(
        "SILICONCLOUD_BASE_URL",
        "https://api.siliconflow.com/v1",
    )
    model = os.getenv("SILICONCLOUD_EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-8B")

    async def embedding_func(texts: list[str] | str) -> np.ndarray:
        if isinstance(texts, str):
            texts = [texts]

        results: list[list[float]] = []

        for i in range(0, len(texts), 2048):
            batch = texts[i : i + 2048]
            safe_batch = [t if t.strip() else " " for t in batch]

            async with httpx.AsyncClient(base_url=base_url, timeout=30.0) as client:
                response = await client.post(
                    "/embeddings",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    json={"model": model, "input": safe_batch},
                )
                response.raise_for_status()
                data = response.json()

            embeddings = data.get("data", [])
            if len(embeddings) != len(safe_batch):
                raise ValueError(
                    f"Embedding count mismatch: sent {len(safe_batch)}, got {len(embeddings)}. "
                    f"Response: {data}"
                )

            for item in embeddings:
                results.append(item["embedding"])

        return np.array(results, dtype=np.float32)

    return EmbeddingFunc(
        embedding_dim=_EMBEDDING_DIM,
        func=embedding_func,
        send_dimensions=False,
        model_name=model,
    )
