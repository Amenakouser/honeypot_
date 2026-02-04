from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router
from .core.firebase import initialize_firebase, check_firebase_health
import os
import asyncio

app = FastAPI(
    title="AI Honeypot Scam Detection API",
    description="API for detecting and engaging with scammers",
    version="1.0.0"
)

# Initialize Firebase on startup
@app.on_event("startup")
async def startup_event():
    initialize_firebase()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint"""
    firebase_health = check_firebase_health()
    return {
        "message": "AI Honeypot Scam Detection API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "firebase_connected": firebase_health
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
