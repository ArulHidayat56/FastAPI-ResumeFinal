from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
import os

API_KEY_HEADER = APIKeyHeader(name="X-API-KEY")
EXPECTED_API_KEY = os.getenv("APP_API_KEY")

async def verify_api_key(api_key: str = Depends(API_KEY_HEADER)):
    if api_key != EXPECTED_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
