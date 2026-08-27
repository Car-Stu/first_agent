import os
from typing import List, Dict, Tuple
from dotenv import load_dotenv
from opik import track
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ.get("HF_TOKEN"),
)

MODEL = "deepseek-ai/DeepSeek-V3-0324"  # ungated, avoids license-wall failures

@track
def generate_ai_response(prompt: str, history: List[Dict[str, str]]) -> Tuple[str, List[Dict[str, str]]]:
    """Sends the transcript (with system prompt injected) to the model and returns the reply."""

    api_payload = list(history)
    if not any(msg["role"] == "system" for msg in api_payload):
        api_payload.insert(0, {"role": "system", "content": "You are a helpful AI assistant."})

    response = client.chat.completions.create(
        model=MODEL,
        messages=api_payload,          
        max_tokens=500,
    )
    ai_message = response.choices[0].message.content  
    return ai_message, history