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


def refactor_code(
    code,
    provider,
    model
):
    """
    Analyze code and suggest
    refactoring improvements.
    """

    logger.info(
        "Refactoring analysis started"
    )

    prompt = f"""
You are a Senior Software Architect.

Review the following code.

Provide:

1. Code Smells
2. Refactoring Suggestions
3. Performance Improvements
4. Readability Improvements
5. Maintainability Improvements
6. Best Practices

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
                "OpenAI refactoring completed"
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

        data = response.json()

        result = data.get(
            "response",
            "No suggestions generated."
        )

        logger.info(
            "Ollama refactoring completed"
        )

        return result

    except Exception as e:

        logger.error(
            f"Refactoring Error: {e}"
        )

        return (
            f"Error generating "
            f"refactoring suggestions: "
            f"{str(e)}"
        )

