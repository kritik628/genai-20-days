## Day 04 – AI Recipe Generator (GenAI Project)

### Project Overview
This project is a GenAI-powered recipe generator that converts user-provided ingredients into a structured, machine-readable recipe.

### Input
- Ingredients (comma-separated)
- Diet preference (vegetarian / vegan / etc.)

### Output
Structured JSON containing:
- Recipe name
- Ingredients list
- Step-by-step instructions
- Nutrition information (calories, protein, carbs, fat)

### Key Features
- Reusable LLM engine with retry and self-correction
- Strict JSON output enforcement
- Schema validation to ensure data correctness
- Role-based prompting (Professional Chef AI)

### Why this matters
Instead of generating plain text, this project produces reliable, structured data suitable for real applications such as mobile apps, APIs, and databases.

### Tech Stack
- Python
- Google Gemini (LLM)
- Prompt Engineering
- JSON validation
