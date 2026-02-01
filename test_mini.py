import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def test_api():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("No API key.")
        return
    
    client = genai.Client(api_key=api_key)
    model_id = "gemini-3-flash-preview"
    
    print(f"Testing Gemini 3: {model_id}...")
    
    try:
        response = client.models.generate_content(
            model=model_id,
            contents="Hello, identify yourself."
        )
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    test_api()
