#%%
# send the prompt to llm and print answer

from prompting import SYSTEM_PROMPT
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

def create_client():

    try:
        import streamlit as st
    except ImportError:
        st = None

    load_dotenv()

    if st is not None:
        try:
            api_key = st.secrets["GOOGLE_API_KEY"]
        except Exception:
            api_key = os.getenv("GOOGLE_API_KEY")
    else:
        api_key = os.getenv("GOOGLE_API_KEY")

    client = genai.Client(api_key=api_key,
                          http_options=types.HttpOptions(
                              retry_options=types.HttpRetryOptions(
                                  attempts=3,
                                  initial_delay=2.0,
                                  http_status_codes=[429, 500, 502, 503, 504])
                                )
            )

    return client

def ask_llm(user_prompt, SYSTEM_PROMPT=SYSTEM_PROMPT, model="gemini-3.5-flash"):
    
    full_prompt = SYSTEM_PROMPT + "\n\n" + user_prompt

    class RAGAnswer(BaseModel):
        executive_summary: str
        technical_explanation: str
        citations: list[str]
        confidence: str

    client = create_client()
    response = client.models.generate_content(
        model=model,
        contents='Say Hello.',
        config={
            "response_mime_type": "application/json",
            "response_schema": RAGAnswer,
        },
    )
    return response.parsed