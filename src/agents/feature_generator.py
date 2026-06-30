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


def generate_features(
    code,
    provider,
    model
):

    logger.info(
        "Feature generation started"
    )

    prompt = f"""
You are a Senior Product Engineer.

Analyze the project.

Suggest:

1. Missing Features
2. Advanced Features
3. User Experience Improvements
4. Scalability Improvements
5. Future Enhancements

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
                "OpenAI feature generation completed"
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
            "No features generated."
        )

        logger.info(
            "Ollama feature generation completed"
        )

        return result

    except Exception as e:

        logger.error(
            f"Feature Generator Error: {e}"
        )

        return (
            f"Error generating features: "
            f"{str(e)}"
        )

