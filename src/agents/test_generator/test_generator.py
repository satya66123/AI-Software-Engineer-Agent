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


def generate_tests(
    code,
    provider,
    model
):

    logger.info(
        "Unit test generation started"
    )

    prompt = f"""
You are a Senior Python Test Engineer.

Generate pytest unit tests for the following code.

Requirements:

1. Use pytest
2. Cover normal cases
3. Cover edge cases
4. Cover exception cases
5. Return only test code

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

            tests = (
                response
                .choices[0]
                .message
                .content
            )

            logger.info(
                "OpenAI unit tests generated"
            )

            return tests

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

        tests = response.json().get(
            "response",
            "No tests generated."
        )

        logger.info(
            "Ollama unit tests generated"
        )

        return tests

    except Exception as e:

        logger.error(
            f"Unit Test Generator Error: {e}"
        )

        return (
            f"Error generating tests: "
            f"{str(e)}"
        )
