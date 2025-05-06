import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class GeminiService:
    """Service to interact with Google's Gemini AI"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    async def generate_response(
        self, 
        prompt: str, 
        learning_preferences: Dict[str, bool] = None,
        context: Optional[str] = None
    ) -> str:
        """
        Generate a response from Gemini based on the prompt and learning preferences
        
        Args:
            prompt: User's question or request
            learning_preferences: Dictionary of learning preferences (visual_aids, simplified_language, etc.)
            context: Additional context about the learning materials or user
            
        Returns:
            AI-generated response formatted as HTML
        """
        try:
            # Default preferences if none provided
            preferences = learning_preferences or {
                "visual_aids": False,
                "simplified_language": False,
                "structured_format": False
            }
            
            # Create a system message that adapts to learning preferences
            system_prompt = self._create_system_prompt(preferences)
            
            # Add context if available
            if context:
                system_prompt += f"\nAdditional context: {context}"
                
            # Create the chat session
            chat = self.model.start_chat(history=[])
            
            # Generate the response
            response = chat.send_message(
                [system_prompt, prompt]
            )
            
            return response.text
            
        except Exception as e:
            print(f"Error generating Gemini response: {e}")
            return f"<p>I'm sorry, I encountered an error: {str(e)}</p>"
    
    def _create_system_prompt(self, preferences: Dict[str, bool]) -> str:
        """Create a system prompt based on learning preferences"""
        
        system_prompt = """
        You are an AI learning assistant for NeuroLearn, a platform designed for neurodivergent learners
        including those with dyslexia, autism, ADHD, and anxiety. Your goal is to provide helpful,
        accessible explanations tailored to different learning needs.
        
        Respond in HTML format that can be rendered in a web application. Use headers (<h3>), 
        paragraphs (<p>), lists (<ul>, <ol>), and other HTML elements to structure your response.
        """
        
        # Add specific instructions based on preferences
        if preferences.get("visual_aids", False):
            system_prompt += """
            Include visual descriptions in your response. When describing visual concepts, use clear 
            spatial language and describe images in detail. Add a <div class="visual-aid"></div> 
            section with text descriptions of helpful visuals.
            """
            
        if preferences.get("simplified_language", False):
            system_prompt += """
            Use simplified language. Avoid complex words, use shorter sentences, and explain 
            technical terms. Aim for approximately a 5th-grade reading level. Break complex 
            concepts into smaller parts.
            """
            
        if preferences.get("structured_format", False):
            system_prompt += """
            Use a highly structured format with clear headings, numbered steps, and bullet points.
            Break information into distinct sections with clear titles.
            """
            
        return system_prompt