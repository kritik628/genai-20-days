import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Always force-load environment variables
load_dotenv(override=True)

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_json(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.2,
    max_retries: int = 2
) -> dict:
    """
    Robust LLM utility with retry and self-correction.
    Treats LLM output as untrusted input.
    """

    full_prompt = f"""
{system_prompt}

User Request:
{user_prompt}
"""

    last_error = None

    for attempt in range(1, max_retries + 2):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
            config=types.GenerateContentConfig(
                temperature=temperature
            )
        )

        raw_text = response.text.strip()

        # Remove markdown code fences
        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "")
            raw_text = raw_text.replace("```", "")
            raw_text = raw_text.strip()

        try:
            return json.loads(raw_text)

        except json.JSONDecodeError as e:
            last_error = str(e)

            # Self-correction prompt
            full_prompt = f"""
The following output is INVALID JSON:

{raw_text}

Fix the JSON syntax and return ONLY valid JSON.
"""
            temperature = 0  # strict mode on retry

    raise ValueError(f"LLM failed after retries. Last error: {last_error}")
def validate_interview_schema(data: dict):
    """
    Validates the schema of interview question output.
    Raises ValueError if schema is invalid.
    """

    if "topic" not in data or not isinstance(data["topic"], str):
        raise ValueError("Invalid or missing 'topic'")

    if "level" not in data or data["level"] not in {"easy", "medium", "hard"}:
        raise ValueError("Invalid or missing 'level'")

    if "questions" not in data or not isinstance(data["questions"], list):
        raise ValueError("Invalid or missing 'questions' list")

    for q in data["questions"]:
        if "question" not in q or not isinstance(q["question"], str):
            raise ValueError("Each question must have a 'question' string")

        if "difficulty" not in q or q["difficulty"] not in {"easy", "medium", "hard"}:
            raise ValueError("Each question must have a valid 'difficulty'")


    
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

    result = generate_json(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.3
    )

    validate_interview_schema(result)
    return result


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
