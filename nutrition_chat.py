import streamlit as st
from google import genai

MODEL_NAME = "gemini-3.5-flash-lite"


def ask_macromate(question):

    api_key = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are MacroMate, a friendly AI nutrition assistant.

Answer the user's nutrition question in simple and clear language.

Rules:
- Keep the answer concise.
- Give general nutrition information.
- Do not provide medical diagnosis.
- If an exact nutritional value depends on portion size or preparation,
  clearly mention that it is an estimate.
- Use simple language suitable for a beginner.

User question:
{question}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.strip()