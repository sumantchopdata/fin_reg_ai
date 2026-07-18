#%%
# send the prompt to llm and print answer

from prompting import SYSTEM_PROMPT
import os
import json
from dotenv import load_dotenv
from google import genai

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

  client = genai.Client(api_key=api_key)

  return client

def ask_llm(user_prompt, SYSTEM_PROMPT=SYSTEM_PROMPT, model="gemini-3.5-flash"):

  full_prompt = SYSTEM_PROMPT + "\n\n" + user_prompt

  client = create_client()
  response = client.models.generate_content(
    model=model,
    contents=full_prompt,
    config={
        "response_mime_type": "application/json"
    }
  )
  return response.text