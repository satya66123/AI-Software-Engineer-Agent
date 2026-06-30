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


def generate_code(
    requirement,
    provider,
    model
):

    logger.info(
        "Code generation started"
    )

    prompt = f"""
You are a Senior Software Engineer.

Generate production-ready code.

Requirements:

{requirement}

Provide:

1. Complete Code
2. Comments
3. Example Usage
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
                "OpenAI code generation completed"
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
            "No code generated."
        )

        logger.info(
            "Ollama code generation completed"
        )

        return result

    except Exception as e:

        logger.error(
            f"Code Generator Error: {e}"
        )

        return (
            f"Error generating code: "
            f"{str(e)}"
        )

