import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=600
    )
    return response.choices[0].message.content.strip()
