from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import google.generativeai as genai

# Create router
router = APIRouter()

# Load API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set!")

# Configure the API key
genai.configure(api_key=api_key)

# Pydantic model
class PromptRequest(BaseModel):
    prompt: str

# Route
@router.post("/generate")
async def generate_message(request: PromptRequest):
    try:
        # FIX: Use GenerativeModel class to create a model instance
        model = genai.GenerativeModel('gemini-2.0-flash-exp')  # Updated model name
        
        # Generate content using the model instance
        response = model.generate_content(request.prompt)
        
        # Access the text from the response
        if not response.text:
            raise HTTPException(status_code=500, detail="The model returned an empty response.")
             
        return {"message": response.text}
        
    except Exception as e:
        print("Gemini API error:", e)
        raise HTTPException(status_code=500, detail=f"Could not generate message: {str(e)}")