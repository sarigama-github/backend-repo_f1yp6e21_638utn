import os
from typing import Any, Dict, List, Optional
from datetime import datetime
from pymongo import MongoClient
import anyio

DATABASE_URL = os.getenv('DATABASE_URL', 'mongodb://localhost:27017')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'app')

_client: Optional[MongoClient] = None
_db = None

def _ensure_client():
    global _client, _db
    if _client is None:
        _client = MongoClient(DATABASE_URL)
        _db = _client[DATABASE_NAME]
    return _db

async def get_db():
    return _ensure_client()

async def create_document(collection_name: str, data: Dict[str, Any]) -> str:
    db = _ensure_client()
    doc = {**data, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()}

    def _insert():
        return db[collection_name].insert_one(doc).inserted_id

    inserted_id = await anyio.to_thread.run_sync(_insert)
    return str(inserted_id)

async def get_documents(collection_name: str, filter_dict: Dict[str, Any] | None = None, limit: int = 20) -> List[Dict[str, Any]]:
    db = _ensure_client()

    def _find():
        cur = db[collection_name].find(filter_dict or {}).limit(limit)
        out = []
        for d in cur:
            d['_id'] = str(d.get('_id'))
            out.append(d)
        return out

    return await anyio.to_thread.run_sync(_find)
