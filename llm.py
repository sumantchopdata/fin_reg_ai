#%%
# send the prompt to llm and print answer

from prompting import SYSTEM_PROMPT

def ask_llm(user_prompt, client, SYSTEM_PROMPT=SYSTEM_PROMPT,
  model="gemini-3.5-flash"):

  full_prompt = SYSTEM_PROMPT + "\n\n" + user_prompt

  response = client.models.generate_content(
    model=model,
    contents=full_prompt
  )
  return response.text