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


def answer_question(
    question,
    chunks,
    provider,
    model
):

    logger.info(
        "Repository Q&A started"
    )

    context = ""

    sources = []

    for item in chunks:

        source = item.get(
            "source",
            "Unknown"
        )

        chunk = item.get(
            "chunk",
            ""
        )

        sources.append(source)

        context += f"""
Source:
{source}

Code:
{chunk}

"""

    prompt = f"""
    You are a Senior Software Engineer performing Repository Question Answering.

    Your task is to answer the user's question ONLY using the retrieved repository context.

    ## Strict Rules

    1. Use ONLY the provided repository context.
    2. Never use external knowledge.
    3. Never guess or hallucinate.
    4. If the answer cannot be found, reply exactly:

    "I could not find the answer in the repository."

    5. Mention filenames whenever appropriate.

    6. When answering about a file:
       • Explain the file's primary purpose.
       • Describe its responsibilities.
       • Mention important functions, classes and variables.
       • Explain how it interacts with other files if shown.
       • Do NOT describe libraries unless they are relevant.

    7. When answering about a function:
       • Explain what it does.
       • Explain inputs.
       • Explain outputs.
       • Explain where it is called if available.

    8. When answering about the project:
       • Explain architecture.
       • Explain modules.
       • Explain workflow.

    9. Prefer information from source code over README files if both discuss the same topic.

    10. Keep the answer concise and technical.

    ## Repository Context

    {context}

    ## Question

    {question}

    ## Output Format

    ### Summary

    ...

    ### Responsibilities

    - ...
    - ...
    - ...

    ### Important Components

    - Function:
    - Class:
    - Variable:

    ### Related Files

    - ...

    ### Notes

    ...
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

            answer = (
                response
                .choices[0]
                .message
                .content
            )

        else:

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

            answer = response.json().get(
                "response",
                "No answer generated"
            )

        logger.info(
            f"Retrieved {len(chunks)} chunks"
        )

        return {
            "answer": answer,
            "sources": list(set(sources)),
            "chunks": chunks
        }

    except Exception as e:

        logger.error(
            f"Q&A Error: {e}"
        )

        return {
            "answer": f"Error: {str(e)}",
            "sources": [],
            "chunks": []
        }

