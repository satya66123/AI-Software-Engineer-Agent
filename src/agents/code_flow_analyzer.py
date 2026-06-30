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


def analyze_code_flow(
    code,
    provider,
    model
):

    logger.info(
        "Code flow analysis started"
    )

    prompt = f"""
You are a Senior Software Engineer.

Explain code execution flow.

Provide:

1. Program Start
2. Function Flow
3. Data Flow
4. Execution Order
5. Summary

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
                "OpenAI code flow analysis completed"
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
            "No flow generated."
        )

        logger.info(
            "Ollama code flow analysis completed"
        )

        return result

    except Exception as e:

        logger.error(
            f"Code Flow Error: {e}"
        )

        return (
            f"Error analyzing code flow: "
            f"{str(e)}"
        )

