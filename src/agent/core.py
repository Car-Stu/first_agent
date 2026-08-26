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

    if len(history)==0:     #If this is a brand new chat, initialize the system prompt persona
        history.append({"role": "system", "content": "You are a helpful AI assistant."})

        history.append({"role": "user", "content": prompt}) #Append your brand new question to the ongoing transcript list
    
    response = client.chat_completion(              #Sends the full transcript sequence to the model
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=history,
        max_tokens=500
    )
    ai_message= response.choices[0].message.content

    history.append({"role": "assistant", "content": ai_message})    #Save the AI's response to the history list so it remembers what it said

    return ai_message, history