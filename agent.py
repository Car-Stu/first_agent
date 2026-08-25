import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient 
from opik import track

# Load the hidden api_key from your .env file (did pip install python_dotenv)
load_dotenv()

# Initialize the native Hugging Face client
# Automatically pick up your HF_TOKEN from the environment
client = InferenceClient(token=os.environ.get('HF_TOKEN'))

print("Sending request to Hugging Face via native InferenceClient.")
user_question = input("Ask me a question- ")

@track  #decorator to watch the function
def ai_agent(prompt):
    response=client.chat_completion(
        model = "Qwen/Qwen2.5-Coder-7B-Instruct",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content

try:
    ai_answer=ai_agent(user_question)
    print("\nAI Response:")
    print(ai_answer)

except Exception as e:
    print(f"\nAn error occurred: {e}")