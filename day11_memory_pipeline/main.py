import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

memory = {}

def llm_call(prompt, temperature=0.3):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=temperature)
    )
    return response.text.strip()

def plan_report(topic):
    prompt = f"Create a 3-section outline for a report about: {topic}"
    outline = llm_call(prompt)
    memory["outline"] = outline
    return outline

def generate_section(section_title):
    prompt = f"Write a professional section about: {section_title}"
    content = llm_call(prompt)
    memory[section_title] = content
    return content

def compile_report():
    report = "FINAL REPORT\n\n"
    for key, value in memory.items():
        if key != "outline":
            report += f"{key}\n{value}\n\n"
    return report

if __name__ == "__main__":
    topic = input("Enter report topic: ")

    print("\nPlanning report structure...\n")
    outline = plan_report(topic)
    print(outline)

    sections = outline.split("\n")
    for sec in sections:
        if sec.strip():
            print(f"\nGenerating section: {sec}")
            print(generate_section(sec))

    print("\nCompiling final report...\n")
    print(compile_report())
