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


def generate_documentation(
    code,
    provider,
    model
):

    logger.info(
        "Documentation generation started"
    )

    prompt = f"""
You are a Senior Software Engineer.

Generate professional documentation
for the following code.

Include:

1. Overview
2. Functions
3. Parameters
4. Returns
5. Dependencies
6. Example Usage

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

            documentation = (
                response
                .choices[0]
                .message
                .content
            )

            logger.info(
                "OpenAI documentation generated"
            )

            return documentation

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

        documentation = response.json().get(
            "response",
            "No documentation generated."
        )

        logger.info(
            "Ollama documentation generated"
        )

        return documentation

    except Exception as e:

        logger.error(
            f"Documentation Error: {e}"
        )

        return (
            f"Error generating documentation: "
            f"{str(e)}"
        )

