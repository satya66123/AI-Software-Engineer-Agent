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


def analyze_multiple_files(
    code,
    provider,
    model
):

    logger.info(
        "Multi-file analysis started"
    )

    prompt = f"""
You are a Senior Software Architect.

Analyze multiple files together.

Provide:

1. File Relationships
2. Imports
3. Dependencies
4. Data Movement
5. Architecture Overview
6. Summary

Files:

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
                "OpenAI multi-file analysis completed"
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
            "Ollama multi-file analysis completed"
        )

        return result

    except Exception as e:

        logger.error(
            f"Multi File Analyzer Error: {e}"
        )

        return (
            f"Error analyzing files: "
            f"{str(e)}"
        )
