from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from ..services.gemini_service import GeminiService

router = APIRouter()

# Initialize the Gemini service
gemini_service = GeminiService()

class AIAssistantRequest(BaseModel):
    """Request schema for AI assistant"""
    prompt: str
    learning_preferences: Dict[str, bool] = {
        "visual_aids": False,
        "simplified_language": False,
        "structured_format": False
    }
    context: Optional[str] = None

class AIAssistantResponse(BaseModel):
    """Response schema for AI assistant"""
    response: str

@router.post("/assistant", response_model=AIAssistantResponse)
async def get_ai_response(request: AIAssistantRequest):
    """
    Get a response from the AI assistant based on user prompt and preferences
    """
    if not request.prompt or len(request.prompt.strip()) == 0:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    try:
        response = await gemini_service.generate_response(
            prompt=request.prompt,
            learning_preferences=request.learning_preferences,
            context=request.context
        )
        
        return AIAssistantResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating AI response: {str(e)}")