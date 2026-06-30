import os
import requests

from openai import OpenAI

OLLAMA_URL = "http://localhost:11434/api/generate"

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_response(
    prompt: str,
    provider: str,
    model: str
) -> str:

    try:

        if provider == "OpenAI":

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return (
                response
                .choices[0]
                .message
                .content
            )

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=300
        )

        response.raise_for_status()

        return response.json().get(
            "response",
            "No response generated."
        )

    except Exception as e:

        return f"Error: {str(e)}"