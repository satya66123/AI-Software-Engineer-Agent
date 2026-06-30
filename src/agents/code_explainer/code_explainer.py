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


def explain_code(
    code,
    provider,
    model
):

    logger.info(
        "Code explanation started"
    )

    prompt = f"""
You are a Senior Software Engineer.

Explain this code in simple English.

Provide:

1. Purpose
2. Functions
3. Inputs
4. Outputs
5. Execution Flow

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

            explanation = (
                response
                .choices[0]
                .message
                .content
            )

            logger.info(
                "OpenAI code explanation completed"
            )

            return explanation

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

        explanation = response.json().get(
            "response",
            "No explanation generated"
        )

        logger.info(
            "Ollama code explanation completed"
        )

        return explanation

    except Exception as e:

        logger.error(
            f"Code Explainer Error: {e}"
        )

        return (
            f"Error generating explanation: "
            f"{str(e)}"
        )

