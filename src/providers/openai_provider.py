from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_openai(
    prompt,
    model="gpt-4o-mini"
):

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content