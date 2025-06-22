from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from text_classifier import SelfHealingTextClassifier
import json
import os
import datetime

app = FastAPI(title="Self-Healing Sentiment Classifier API")

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Input model
class TextInput(BaseModel):
    text: str
    confidence_threshold: Optional[float] = 0.7  # Default threshold is 70%

# Initialize classifier
classifier = SelfHealingTextClassifier()

# Logging function
def log_result(input_text: str, result: dict):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"log_{timestamp}.txt"
    log_path = os.path.join(LOG_DIR, log_filename)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Input: {input_text}\n")
        f.write(f"Prediction: {result['prediction']}\n")
        f.write(f"Confidence: {result['confidence']}\n")
        f.write(f"Used Fallback: {result['used_fallback']}\n")

# POST endpoint
@app.post("/classify")
async def classify_sentiment(input_data: TextInput):
    """
    Classify the sentiment of the input text and log the result.
    """
    try:
        # Classify the text
        result = classifier.classify_with_fallback(input_data.text)
        
        # Round confidence
        result['confidence'] = round(result['confidence'], 1)

        # Log result
        log_result(input_data.text, result)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

# Root GET endpoint
@app.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Welcome to the Self-Healing Sentiment Classifier API",
        "endpoints": {
            "POST /classify": {
                "description": "Classify sentiment of text",
                "example": {
                    "text": "I absolutely loved this movie!",
                    "confidence_threshold": 0.7
                }
            }
        }
    }
