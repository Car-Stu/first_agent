import sys
import os

# Ensure Python can find local src/ folder during tests
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the core function to validate
from src.agent.core import generate_ai_response

def test_generate_ai_response_is_string():
    #Verify that our core backend function returns a valid text string
    test_prompt = "Hello"
    
    # Run the function with a quick test prompt
    result = generate_ai_response(test_prompt)
    
    # Assert checks if the condition is True. If False, the test fails.
    assert isinstance(result, str), "The AI response should be a text string."
    assert len(result) > 0, "The AI response should not be empty."
