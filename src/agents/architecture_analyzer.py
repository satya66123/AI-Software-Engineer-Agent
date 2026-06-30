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


def analyze_architecture(
    code,
    provider,
    model
):
    """
    Analyze project architecture.
    """

    logger.info(
        "Architecture analysis started"
    )

    prompt = f"""
You are a Senior Software Architect.

Analyze the project architecture.

Provide:

1. Architecture Pattern
2. Main Components
3. Module Relationships
4. Data Flow
5. Recommendations

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
                "OpenAI architecture analysis completed"
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
            "No architecture generated."
        )

        logger.info(
            "Ollama architecture analysis completed"
        )

        return result

    except Exception as e:

        logger.error(
            f"Architecture Analyzer Error: {e}"
        )

        return (
            f"Error analyzing architecture: "
            f"{str(e)}"
        )

