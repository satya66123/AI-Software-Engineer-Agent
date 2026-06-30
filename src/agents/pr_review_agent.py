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


def review_pull_request(
    code,
    provider,
    model
):

    logger.info(
        "PR review started"
    )

    prompt = f"""
You are a Senior Pull Request Reviewer.

Analyze this code change.

Provide:

1. Summary
2. Risks
3. Breaking Changes
4. Suggestions
5. Approval Recommendation

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
                "OpenAI PR review completed"
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
            "No PR review generated."
        )

        logger.info(
            "Ollama PR review completed"
        )

        return result

    except Exception as e:

        logger.error(
            f"PR Review Error: {e}"
        )

        return (
            f"Error reviewing pull request: "
            f"{str(e)}"
        )

