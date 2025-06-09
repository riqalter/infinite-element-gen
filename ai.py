import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

api_key: str = os.getenv("GEMINI_API_KEY", "No API Key Found")

client: genai.Client = genai.Client(api_key=api_key)

def generate_craft(first_element: str, second_element: str) -> str | None:
    system_instruction: str = (
        "You are a whimsical crafting game AI. The user will give you two items, and your task is to "
        "tell them what new item they've created by combining them. The result should be a single, "
        "concise concept. Your response must be a JSON object with two keys: 'result' (the name of the "
        "new item as a string) and 'emoji' (a single emoji representing the new item as a string)."
    )

    prompt: str = f"Combine '{first_element}' and '{second_element}'."

    schema: dict[str, dict[str, dict[str, str]] | list[str] | str] = {
        "type": "OBJECT",
        "properties": {
            "result": {"type": "STRING"},
            "emoji": {"type": "STRING"}
        },
        "required": ["result", "emoji"]
    }

    response: types.GenerateContentResponse = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=[prompt],
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=schema,
            temperature=0.7,
            seed=42,
        )
    )
    
    return response.text
