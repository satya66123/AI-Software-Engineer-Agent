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


def review_code(
    code,
    provider,
    model
):

    logger.info(
        "Code review started"
    )

    prompt = f"""
You are a Senior Software Engineer.

Review the following code.

Provide:

1. Code Quality Score
2. Best Practices
3. Readability Issues
4. Maintainability Issues
5. Performance Suggestions
6. Final Review Summary

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
                "OpenAI code review completed"
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
            "No review generated."
        )

        logger.info(
            "Ollama code review completed"
        )

        return result

    except Exception as e:

        logger.error(
            f"Code Review Error: {e}"
        )

        return (
            f"Error reviewing code: "
            f"{str(e)}"
        )
