import json
from google import genai
from google.genai import types
import streamlit as st


MODEL_NAME = "gemini-3.5-flash-lite"


def analyze_meal(uploaded_image):

    api_key = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(
        api_key=api_key
    )

    image_part = types.Part.from_bytes(
        data=uploaded_image.getvalue(),
        mime_type=uploaded_image.type
    )

    prompt = """
You are MacroMate, an AI nutrition assistant.

Analyze the food shown in the image.

Identify:
1. The food items visible
2. Estimated total calories
3. Estimated protein in grams
4. Estimated carbohydrates in grams
5. Estimated fat in grams
6. A short nutrition summary

Return ONLY valid JSON.

Use exactly this format:

{
    "food_detected": "food items",
    "calories": 0,
    "protein": 0,
    "carbs": 0,
    "fat": 0,
    "summary": "short nutrition summary"
}

Important:
- Nutritional values are estimates.
- Consider the visible portion size.
- Do not claim medical accuracy.
- If the food cannot be identified clearly, say so.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            image_part,
            prompt
        ]
    )

    text = response.text.strip()

    # Remove markdown code fences if Gemini adds them
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)