import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(override=True)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_json(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.2,
    max_retries: int = 2
) -> dict:
    """
    Reusable LLM engine with retry and self-correction
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
            temperature = 0

    raise ValueError(f"LLM failed after retries: {last_error}")

def validate_recipe_schema(data: dict):
    if "recipe_name" not in data or not isinstance(data["recipe_name"], str):
        raise ValueError("Missing or invalid recipe_name")

    if "ingredients" not in data or not isinstance(data["ingredients"], list):
        raise ValueError("Missing or invalid ingredients list")

    if "steps" not in data or not isinstance(data["steps"], list):
        raise ValueError("Missing or invalid steps list")

    if "nutrition" not in data or not isinstance(data["nutrition"], dict):
        raise ValueError("Missing or invalid nutrition info")

    for key in ["calories", "protein", "carbs", "fat"]:
        if key not in data["nutrition"]:
            raise ValueError(f"Missing nutrition field: {key}")



def recipe_generator(ingredients: str, diet: str = "vegetarian") -> dict:
    """
    Generates a recipe using given ingredients and diet preference.
    """

    system_prompt = """
You are a professional chef AI.
You generate simple, realistic recipes.

Rules:
- Return ONLY valid JSON
- Do NOT include explanations or extra text
- Recipe must match the diet preference

JSON format:
{
  "recipe_name": "string",
  "ingredients": ["string"],
  "steps": ["string"],
  "nutrition": {
    "calories": "string",
    "protein": "string",
    "carbs": "string",
    "fat": "string"
  }
}
"""

    user_prompt = f"""
Create a {diet} recipe using the following ingredients:
{ingredients}
"""

    result = generate_json(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.4
    )

    validate_recipe_schema(result)
    return result



if __name__ == "__main__":
    ingredients = input("Enter ingredients (comma separated): ")
    diet = input("Enter diet (vegetarian / vegan / etc): ")

    result = recipe_generator(ingredients, diet)

    print("\nGenerated Recipe:\n")
    print(json.dumps(result, indent=2))
