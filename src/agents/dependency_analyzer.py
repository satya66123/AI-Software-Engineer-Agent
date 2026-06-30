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


def analyze_dependencies(
    code,
    provider,
    model
):

    logger.info(
        "Dependency analysis started"
    )

    prompt = f"""
You are a Senior Software Architect.

Analyze the following codebase imports.

Provide:

1. Dependencies Used
2. Purpose of Each Dependency
3. Unused Dependencies
4. Missing Dependencies
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
                "OpenAI dependency analysis completed"
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
            "No analysis generated."
        )

        logger.info(
            "Ollama dependency analysis completed"
        )

        return result

    except Exception as e:

        logger.error(
            f"Dependency Analyzer Error: {e}"
        )

        return (
            f"Error analyzing dependencies: "
            f"{str(e)}"
        )

