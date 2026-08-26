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

     # 1. Clean out any empty string entries that might have corrupted the state array
    history = [msg for msg in history if msg.get("content")]

    # 2. Inject system context at the very front if it's missing
    if not any(msg["role"] == "system" for msg in history):
        history.insert(0, {"role": "system", "content": "You are a helpful AI assistant."})

    response = client.chat.completions.create(              #Sends the full transcript sequence to the model
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=history,
        max_tokens=500
    )
    ai_message= response.choices[0].message.content

    history.append({"role": "assistant", "content": ai_message})    #Save the AI's response to the history list so it remembers what it said

    return ai_message, history