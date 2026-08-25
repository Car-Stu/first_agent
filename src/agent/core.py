import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from opik import track

# Load configuration values safely
load_dotenv()

# Initialize the Hugging Face client
client = InferenceClient(token=os.environ.get("HF_TOKEN"))

@track  # Automatically track this specific logic function in Opik
def generate_ai_response(prompt: str) -> str:
    #Sends a user prompt to the model and returns the text response
    response = client.chat_completion(
        model="Qwen/Qwen2.5-Coder-7B-Instruct",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content