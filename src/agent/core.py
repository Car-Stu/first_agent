import os
from typing import List, Dict, Tuple
from dotenv import load_dotenv
#from huggingface_hub import InferenceClient
from opik import track
from openai import OpenAI # Standardize the connection using the OpenAI client layout

# Load configuration values safely
load_dotenv()
# Initialize the Hugging Face client
client = OpenAI(
    base_url="https://router.huggingface.co/v1", # Swapped to the correct backend route
    api_key=os.environ.get("HF_TOKEN"))

@track  # Automatically track this specific logic function in Opik
def generate_ai_response(prompt: str, history: List[Dict[str,str]]) -> tuple[str, List[Dict[str,str]]]:
    """Appends new messages to the chat history, requests a completion, and returns the response."""

    # 1. Create a safe, temporary copy of the history list to pass to the API
    api_payload = list(history)
    
    # 2. Add system context at the very front of our payload array if it's missing
    if not any(msg["role"] == "system" for msg in api_payload):
        api_payload.insert(0, {"role": "system", "content": "You are a helpful AI assistant."})

    response = client.chat.completions.create(              #Sends the full transcript sequence to the model
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=history,
        max_tokens=500
    )
    ai_message= response.choices.message.content

    return ai_message, history