import sys
import streamlit as st
from src.agent.core import generate_ai_response # Import backend function from module layout

def main():
    st.set_page_config(page_title="My AI Assistant")    # Set up a clean browser window title and header. Using streamlit st instead of print statements because in the dashboard the print/input are not possible because there is no keyboard attached to the cloud server 
    st.title("My local Assistant")
    st.write("A stateful AI agent deployed with full CI/CD and Opik tracing.")
    
    # 2. Initialize Streamlit's web-safe persistent memory array
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 3. Render all past messages in the browser window dynamically
    # We skip the system prompt at index 0 so it stays hidden from users
    for message in st.session_state.chat_history:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # 4. Create a native web typing input bar at the bottom
    if user_question := st.chat_input("Ask me anything"):
        
        # Display your newly typed question instantly on screen
        with st.chat_message("user"):
            st.write(user_question)

        # Trigger a beautiful animated loading spinner while the AI thinks
        with st.spinner("Thinking..."):
            try:
                # Pass the question and history tracking variables down the pipe
                ai_answer, updated_history = generate_ai_response(
                    user_question, 
                    st.session_state.chat_history
                )
                
                # Save the new conversation state back to the web session memory
                st.session_state.chat_history = updated_history
                
                # Display the AI's response text block cleanly
                with st.chat_message("assistant"):
                    st.write(ai_answer)
                    
            except Exception as e:
                st.error(f"An application error occurred: {e}")

if __name__ == "__main__":
    main()