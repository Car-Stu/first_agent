import sys
import streamlit as st
from src.agent.core import generate_ai_response # Import backend function from module layout

def main():
    st.set_page_config(page_title="My AI Assistant")    # Set up a clean browser window title and header. Using streamlit st instead of print statements because in the dashboard the print/input are not possible because there is no keyboard attached to the cloud server 
    st.title("My local Assistant")
    st.write("A stateful AI agent deployed with full CI/CD and Opik tracing.")
    
    # Initialize Streamlit's web-safe persistent memory array
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Render all past messages in the browser window dynamically
    # We skip the system prompt at index 0 so it stays hidden from users
    for message in st.session_state.chat_history:
        if message["role"] != "system" and message.get("content"):
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # Create a native web typing input bar at the bottom
    if user_question := st.chat_input("Ask me anything"):
        st.session_state.chat_history.append({"role": "user", "content": user_question})

        with st.chat_message("user"):
            st.write(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    ai_answer, _ = generate_ai_response(user_question, st.session_state.chat_history)
                    if ai_answer and ai_answer.strip():
                        st.session_state.chat_history.append({"role": "assistant", "content": ai_answer})
                        st.write(ai_answer)
                    else:
                        st.error("Empty response.")
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    main()