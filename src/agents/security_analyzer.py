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


def analyze_security(
    code,
    provider,
    model
):

    logger.info(
        "Security analysis started"
    )

    prompt = f"""
You are a Senior Application Security Engineer.

Analyze the following code.

Provide:

1. Security Vulnerabilities
2. Sensitive Data Exposure
3. Authentication Issues
4. Authorization Issues
5. Secure Coding Recommendations
6. Risk Level

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
                "OpenAI security analysis completed"
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
            "No security issues found."
        )

        logger.info(
            "Ollama security analysis completed"
        )

        return result

    except Exception as e:

        logger.error(
            f"Security Analyzer Error: {e}"
        )

        return (
            f"Error analyzing security: "
            f"{str(e)}"
        )
