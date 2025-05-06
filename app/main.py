from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

# Import our API router
from app.api.resources import router as resources_router
# Import database functions
from app.models.database import create_tables

# Load environment variables from .env file
load_dotenv()

# Create the FastAPI application
app = FastAPI(
    title="NeuroLearn API",
    description="API for NeuroLearn - A learning platform for neurodivergent individuals",
    version="0.1.0"
)

# Configure CORS to allow requests from our Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our routers
app.include_router(resources_router, prefix="/api", tags=["Learning Resources"])

# Create database tables
create_tables()

# Basic health check endpoint
@app.get("/")
async def root():
    return {"status": "online", "message": "Welcome to NeuroLearn API"}

# Run the API with uvicorn
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)