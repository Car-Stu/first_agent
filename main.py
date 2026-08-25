import sys
from src.agent.core import generate_ai_response # Import backend function from module layout

def main():
    print("My local Assistant")
    user_question = input("Ask me anything - ")

    # Basic structural verification guardrail
    if not user_question.strip():
        print("Error:Prompt is empty")
        sys.exit(1)

    try:
        ai_answer=generate_ai_response(user_question)

        print("\nAI Response: ")
        print(ai_answer)

    except Exception as e:
        print(f"\nAn application error occurred: {e}")

if __name__ == "__main__":
    main()