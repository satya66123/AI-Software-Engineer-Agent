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


def find_bugs(
    code,
    provider,
    model
):

    logger.info(
        "Bug analysis started"
    )

    prompt = f"""
You are a Senior Software Engineer.

Analyze the following code and find:

1. Bugs
2. Logic Errors
3. Performance Issues
4. Security Risks
5. Code Smells
6. Improvement Suggestions

Provide clear explanations.

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
                "OpenAI bug analysis completed"
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
            "No bugs found."
        )

        logger.info(
            "Ollama bug analysis completed"
        )

        return result

    except Exception as e:

        logger.error(
            f"Bug Finder Error: {e}"
        )

        return (
            f"Error analyzing code: "
            f"{str(e)}"
        )

