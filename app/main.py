from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

from app.api.resources import router as resources_router
from app.api.aiassistant import router as ai_assistant_router

from app.models.database import create_tables


load_dotenv()

app = FastAPI(
    title="NeuroLearn API",
    description="API for NeuroLearn - A learning platform for neurodivergent individuals",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(resources_router, prefix="/api", tags=["Learning Resources"])
app.include_router(ai_assistant_router, prefix="/api", tags=["AI Assistant"])


create_tables()

@app.get("/")
async def root():
    return {"status": "online", "message": "Welcome to NeuroLearn API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)