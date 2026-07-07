#%%
# send the prompt to llm and print answer

from ollama import chat
from prompting import SYSTEM_PROMPT, user_prompt

def ask_llm(user_prompt, SYSTEM_PROMPT=SYSTEM_PROMPT, model="qwen2.5:7b"):

    response = chat(
        model=model,
        messages=[

        {
            "role":"system",
            "content":SYSTEM_PROMPT
        },

        {
            "role":"user",
            "content":user_prompt
        }

    ]
    )

    return response["message"]["content"]
#%%