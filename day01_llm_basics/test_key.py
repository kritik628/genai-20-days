import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GEMINI_API_KEY")

print("KEY VALUE:", key)
print("KEY LENGTH:", len(key) if key else "NO KEY")
