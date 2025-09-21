from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from .routes import router
from .agent import SystemDesignAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="System Design Assistant",
    description="AI-powered system design learning platform",
    version="0.1.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    logger.info("System Design Assistant API starting up...")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "sda-api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

