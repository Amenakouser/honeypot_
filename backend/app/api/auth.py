from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

API_SECRET_KEY = os.getenv("API_SECRET_KEY", "your_secret_key_here")


async def validate_api_key(api_key: str = Security(api_key_header)):
    """Validate API key from request header"""
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key"
        )
    
    if api_key != API_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return api_key
