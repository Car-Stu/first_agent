import sys
from src.agent.core import generate_ai_response # Import backend function from module layout

def main():
    print("My local Assistant")
    
    chat_history= []    # Initialize an empty list to act as agent's short-term memory

    while True:
        user_question = input("Ask me anything - ")

        if user_question.strip().lower() in ['exit','quit']:
            print("Goodbye")
            break
    # Basic structural verification guardrail
        if not user_question.strip():
            print("Error:Prompt is empty")
            continue

        try:
            ai_answer,updated_history = generate_ai_response(user_question, chat_history) #Pass the question AND your running history to the backend

            chat_history = updated_history #Save the updated history for the next loop iteration
            print("\nAI Response: ")
            print(ai_answer)

        except Exception as e:
            print(f"\nAn application error occurred: {e}")

if __name__ == "__main__":
    main()