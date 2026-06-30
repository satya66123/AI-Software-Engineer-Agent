import os
import requests

from openai import OpenAI

from src.utils.logger import logger

OLLAMA_URL = "http://localhost:11434/api/generate"

client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)


def generate_api_docs(
    code,
    provider,
    model
):

    logger.info(
        "API documentation generation started"
    )

    prompt = f"""
You are a Senior API Documentation Engineer.

Generate API documentation.

Include:

1. Functions
2. Parameters
3. Return Values
4. Usage Examples
5. Notes

Code:

{code}
"""

    try:

        # OpenAI
        if provider == "OpenAI":

            response = (
                client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
            )

            result = (
                response
                .choices[0]
                .message
                .content
            )

            logger.info(
                "OpenAI API documentation generated"
            )

            return result

        # Ollama
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

        result = response.json().get(
            "response",
            "No documentation generated."
        )

        logger.info(
            "Ollama API documentation generated"
        )

        return result

    except Exception as e:

        logger.error(
            f"API Documentation Error: {e}"
        )

        return (
            f"Error generating API docs: "
            f"{str(e)}"
        )

