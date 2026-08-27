import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.agent.core import generate_ai_response

def test_generate_ai_response_is_string():
    """Verify that our core backend function returns text and history."""
    test_prompt = "Hello"
    empty_history = [] # Add a mock empty memory list for the test runner
    
    # Update the function call to match our new signature
    result, updated_history = generate_ai_response(test_prompt, empty_history)
    
    assert isinstance(result, str), "The AI response should be a text string."
    assert len(result) > 0, "The AI response should not be empty."
    assert updated_history == empty_history, "core.py should not mutate history."
