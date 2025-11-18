from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from schemas import Contact
from database import create_document, get_documents, get_db
import os

app = FastAPI(title="Portfolio API")

# CORS
frontend_url = os.getenv('FRONTEND_URL', '*')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Backend running"}

@app.get("/test")
async def test_db():
    try:
        db = await get_db()
        collections = await db.list_collection_names()
        return {
            "backend": "ok",
            "database": "mongo",
            "database_url": os.getenv('DATABASE_URL', 'mongodb://localhost:27017'),
            "database_name": os.getenv('DATABASE_NAME', 'app'),
            "connection_status": "connected",
            "collections": collections,
        }
    except Exception as e:
        return {"backend": "ok", "database": "error", "error": str(e)}

@app.post("/contact")
async def contact_submit(payload: Contact):
    try:
        _id = await create_document('contact', payload.model_dump())
        return {"status": "ok", "id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
