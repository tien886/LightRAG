"""FastAPI server — exposes UIT Buddy Backend APIs to BuddyAI."""
from __future__ import annotations
from fastapi.responses import RedirectResponse

from typing import Annotated

from fastapi import FastAPI, Header, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from config.app_config import SERVER_HOST, SERVER_PORT
from service.backend.buddy_service import get_buddy_service
from client.buddy_client import UITBuddyClient
from exception.buddy.buddy_exception import BackendAPIError

from controller.chat_controller import router as chat_router
from controller.rag_controller import router as rag_router

app = FastAPI(
    title="BuddyAI — UIT Buddy Backend Proxy + RAG",
    description="Proxies authenticated requests to UIT Buddy Backend and provides academic RAG.",
    version="1.0.0",
)

app.include_router(chat_router)
app.include_router(rag_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def validate_token(authorization: str) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = authorization.strip()

    parts = token.split(".")

    if len(parts) != 3:
        raise HTTPException(
            status_code=401,
            detail="Invalid token format (expected JWT with 3 parts)"
        )

    return token

@app.get("/")
async def root():
    return RedirectResponse("/docs")


@app.get("/api/schedule/deadline")
async def get_deadlines(
    authorization: str | None = Header(default=None),
    page: int = 1,
    limit: int = 15,
    sortType: str = "desc",
    sortBy: str = "created_at",
    month: int = 1,
    year: int = 1,
):
    print(authorization)
    token = validate_token(authorization)
    print("LLM calling get deadlines")
    try:
        return await get_buddy_service ().get_deadlines(
            token=token,
            page=page,
            limit=limit,
            sortType=sortType,
            sortBy=sortBy,
            month=month,
            year=year,
        )
    except BackendAPIError as e:
        raise HTTPException(status_code=e.status_code, detail={"code": e.code, "message": e.detail})


@app.post("/api/schedule/deadline")
async def create_deadline(
    authorization: str | None = Header(default=None),
    exerciseName: str = "",
    classCode: str = "",
    dueDate: str = "",
):
    token = validate_token(authorization)
    print("LLM calling create deadlines")
    try:
        return await get_buddy_service ().create_deadline(
            token=token,
            exerciseName=exerciseName,
            classCode=classCode,
            dueDate=dueDate,
        )
    except BackendAPIError as e:
        raise HTTPException(status_code=e.status_code, detail={"code": e.code, "message": e.detail})


@app.get("/api/schedule/calendar")
async def get_calendar(
    authorization: str | None = Header(default=None),
    year: str = "",
    semester: str = "",
):
    token = validate_token(authorization)
    try:
        return await get_buddy_service ().get_calendar(
            token=token,
            year=year,
            semester=semester,
        )
    except BackendAPIError as e:
        raise HTTPException(status_code=e.status_code, detail={"code": e.code, "message": e.detail})



@app.get("/api/user/me")
async def get_user_me(
    authorization: str | None = Header(default=None),
):
    token = validate_token(authorization)
    print("LLM calling get user")
    try:
        return await get_buddy_service ().get_user_profile(token=token)
    except BackendAPIError as e:
        raise HTTPException(status_code=e.status_code, detail={"code": e.code, "message": e.detail})



@app.get("/api/document/folder")
async def get_folder(
    authorization: str | None = Header(default=None),
    folderId: str = "",
    page: int = 1,
    limit: int = 15,
    sortType: str = "desc",
    sortBy: str = "createdAt",
):
    token = validate_token(authorization)
    print("LLM calling get folder")
    try:
        return await get_buddy_service ().get_folder(
            token=token,
            folderId=folderId,
            page=page,
            limit=limit,
            sortType=sortType,
            sortBy=sortBy,
        )
    except BackendAPIError as e:
        raise HTTPException(status_code=e.status_code, detail={"code": e.code, "message": e.detail})


@app.get("/api/document/search")
async def search_documents(
    authorization: str | None = Header(default=None),
    keyword: str = "",
    page: int = 1,
    limit: int = 15,
    sortType: str = "desc",
    sortBy: str = "createdAt",
):
    token = validate_token(authorization)
    print("LLM calling search documents")
    try:
        return await get_buddy_service ().search_documents(
            token=token,
            keyword=keyword,
            page=page,
            limit=limit,
            sortType=sortType,
            sortBy=sortBy,
        )
    except BackendAPIError as e:
        raise HTTPException(status_code=e.status_code, detail={"code": e.code, "message": e.detail})


@app.get("/api/document/download/{fileId}")
async def download_document(
    authorization: str | None = Header(default=None),
    fileId: str = "",
):
    token = validate_token(authorization)
    print("LLM calling download document")
    try:
        content = await get_buddy_service ().download_document(
            token=token,
            fileId=fileId,
        )
        return Response(
            content=content,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f'attachment; filename="{fileId}"'},
        )
    except BackendAPIError as e:
        raise HTTPException(status_code=e.status_code, detail={"code": e.code, "message": e.detail})



@app.get("/health")
async def health():
    client = UITBuddyClient()
    response = client.get(path="/docs", token=None, params=None)
    if( response is None):
        return {"status": "error", "detail": "Cannot reach UIT Buddy Backend"}
    return {"status": "ok"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
