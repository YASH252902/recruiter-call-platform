import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_call_script(candidate_id: str) -> str:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"Write a short, friendly opening line for a recruiter calling candidate {candidate_id} about a software engineering role."
    )
    return response.text