import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Always force-load environment variables
load_dotenv(override=True)

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_json(system_prompt: str, user_prompt: str, temperature: float = 0.2) -> dict:
    """
    Generic utility function to get JSON-safe output from Gemini.
    This function will be reused across multiple projects.
    """

    full_prompt = f"""
{system_prompt}

User Request:
{user_prompt}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt,
        config=types.GenerateContentConfig(
            temperature=temperature
        )
    )

    raw_text = response.text.strip()

    # Remove markdown code fences if present
    if raw_text.startswith("```"):
        raw_text = raw_text.replace("```json", "")
        raw_text = raw_text.replace("```", "")
        raw_text = raw_text.strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON returned by LLM:\n{raw_text}")
    
def interview_question_generator(topic: str, level: str = "medium") -> dict:
    """
    Generates interview questions for a given topic and difficulty level
    """

    system_prompt = """
You are a senior technical interviewer at a FAANG-level company.
You ask clear, practical, and conceptually strong interview questions.

Rules:
- Return ONLY valid JSON
- Do NOT include explanations or extra text
- Questions must match the difficulty level

JSON format:
{
  "topic": "string",
  "level": "easy | medium | hard",
  "questions": [
    {
      "question": "string",
      "difficulty": "easy | medium | hard"
    }
  ]
}
"""

    user_prompt = f"""
Generate exactly 5 interview questions on the topic: {topic}
Difficulty level: {level}
"""

    return generate_json(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.3
    )

if __name__ == "__main__":
    system_prompt = """
You are a strict JSON generator.
Return ONLY valid JSON.

JSON format:
{
  "message": "string"
}
"""

    user_prompt = "Say hello in one sentence."

    result = generate_json(system_prompt, user_prompt)
    print(result)
if __name__ == "__main__":
    topic = input("Enter topic: ")
    level = input("Enter difficulty (easy / medium / hard): ")

    result = interview_question_generator(topic, level)

    print("\nGenerated Interview Questions:\n")
    print(json.dumps(result, indent=2))
