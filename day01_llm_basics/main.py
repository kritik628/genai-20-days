import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_json_response(prompt: str) -> dict:
    """
    Sends prompt to Gemini and enforces valid JSON output
    """

    system_prompt = f"""
You are a strict JSON generator.
Return ONLY valid JSON.
Do NOT add explanations or extra text.

JSON format:
{{
  "answer": "string"
}}

Prompt:
{prompt}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=system_prompt,
        config=types.GenerateContentConfig(
            temperature=0
        )
    )

    raw_text = response.text.strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON returned by LLM:\n{raw_text}")

if __name__ == "__main__":
    user_prompt = input("Enter your question: ")

    try:
        result = get_json_response(user_prompt)
        print("\nParsed JSON Output:")
        print(result)
    except Exception as e:
        print("Error:", e)
