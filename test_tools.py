import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def test_tools():
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    # Minimal tool config matching our agent.py
    def get_tools():
        return [
            types.FunctionDeclaration(
                name="list_processes",
                description="Check running processes for resource usage.",
                parameters=types.Schema(type="OBJECT", properties={})
            )
        ]

    print("Attempting to call Gemini with tools...")
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents="Identify a high CPU process.",
            config=types.GenerateContentConfig(
                tools=[types.Tool(function_declarations=get_tools())]
            )
        )
        print("Success!")
        print(response.candidates[0].content.parts[0])
    except Exception as e:
        print(f"FAILED with error: {e}")

if __name__ == "__main__":
    test_tools()
