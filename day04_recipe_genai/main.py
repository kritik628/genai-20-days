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
    if "recipes" not in data or not isinstance(data["recipes"], list):
        raise ValueError("Missing or invalid recipes list")

    if len(data["recipes"]) != 3:
        raise ValueError("Expected exactly 3 recipes")

    for recipe in data["recipes"]:
        required_fields = [
            "recipe_name",
            "difficulty",
            "cook_time_minutes",
            "ingredients",
            "steps",
            "nutrition"
        ]

        for field in required_fields:
            if field not in recipe:
                raise ValueError(f"Missing field in recipe: {field}")

        if recipe["difficulty"] not in {"easy", "medium", "hard"}:
            raise ValueError("Invalid difficulty value")

        if not isinstance(recipe["cook_time_minutes"], int):
            raise ValueError("cook_time_minutes must be an integer")

        for key in ["calories", "protein", "carbs", "fat"]:
            if key not in recipe["nutrition"]:
                raise ValueError(f"Missing nutrition field: {key}")


def rank_recipes(recipes: list) -> list:
    """
    Ranks recipes by cook time (ascending) and difficulty.
    """

    difficulty_order = {
        "easy": 1,
        "medium": 2,
        "hard": 3
    }

    return sorted(
        recipes,
        key=lambda r: (
            r["cook_time_minutes"],
            difficulty_order.get(r["difficulty"], 99)
        )
    )


def recipe_generator(ingredients: str, diet: str = "vegetarian") -> dict:
    """
    Generates recipes using given ingredients and diet preference.
    """

    system_prompt = """
You are a professional chef AI.
You generate simple, realistic recipes.

Rules:
- Return ONLY valid JSON
- Do NOT include explanations or extra text
- Recipes must match the diet preference

JSON format:
{
  "recipes": [
    {
      "recipe_name": "string",
      "difficulty": "easy | medium | hard",
      "cook_time_minutes": number,
      "ingredients": ["string"],
      "steps": ["string"],
      "nutrition": {
        "calories": "string",
        "protein": "string",
        "carbs": "string",
        "fat": "string"
      }
    }
  ]
}
"""

    user_prompt = f"""
Generate exactly 3 {diet} recipes using the following ingredients:
{ingredients}
"""

    result = generate_json(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.4
    )

    validate_recipe_schema(result)

    ranked = rank_recipes(result["recipes"])
    result["recipes"] = ranked

    return result


if __name__ == "__main__":
    ingredients = input("Enter ingredients (comma separated): ")
    diet = input("Enter diet (vegetarian / vegan / etc): ")

    result = recipe_generator(ingredients, diet)

    print("\nGenerated Recipes:\n")
    print(json.dumps(result, indent=2))
