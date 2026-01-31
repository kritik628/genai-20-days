import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --------------------------------------------------
# ENV + CLIENT SETUP
# --------------------------------------------------

load_dotenv(override=True)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --------------------------------------------------
# REUSABLE GENAI ENGINE
# --------------------------------------------------

def generate_json(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.2,
    max_retries: int = 2
) -> dict:
    """
    Reusable LLM engine with retry and self-correction.
    Treats LLM output as untrusted input.
    """

    full_prompt = f"""
{system_prompt}

User Request:
{user_prompt}
"""

    last_error = None

    for _ in range(max_retries + 1):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
            config=types.GenerateContentConfig(
                temperature=temperature
            )
        )

        raw_text = response.text.strip()

        # Remove markdown fences if present
        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "")
            raw_text = raw_text.replace("```", "")
            raw_text = raw_text.strip()

        try:
            return json.loads(raw_text)

        except json.JSONDecodeError as e:
            last_error = str(e)
            full_prompt = f"""
The following output is INVALID JSON:

{raw_text}

Fix the JSON and return ONLY valid JSON.
"""
            temperature = 0  # strict retry

    raise ValueError(f"LLM failed after retries: {last_error}")

# --------------------------------------------------
# RESUME BULLET GENERATOR (PROJECT #2 CORE)
# --------------------------------------------------

def resume_bullet_generator(
    role: str,
    skills: str,
    experience_level: str = "fresher"
) -> dict:
    """
    Generates structured resume bullets for a given role and skills.
    """

    system_prompt = """
You are a professional resume writer AI.

Rules:
- Return ONLY valid JSON
- Do NOT include explanations or extra text
- Bullets must be concise, impact-focused, and resume-ready

JSON format:
{
  "bullets": [
    {
      "bullet": "string",
      "impact": "string",
      "strength": "weak | medium | strong"
    }
  ]
}
"""

    user_prompt = f"""
Generate exactly 5 resume bullets for the following profile:

Role: {role}
Skills: {skills}
Experience Level: {experience_level}

Focus on action verbs, measurable impact, and clarity.
"""

    return generate_json(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.3
    )

# --------------------------------------------------
# CLI ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    role = input("Enter target role: ")
    skills = input("Enter skills (comma separated): ")
    level = input("Enter experience level (fresher / intern / experienced): ")

    result = resume_bullet_generator(role, skills, level)

    print("\nGenerated Resume Bullets:\n")
    print(json.dumps(result, indent=2))
