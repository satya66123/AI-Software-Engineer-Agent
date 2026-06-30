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


def rerank_chunks(
    question,
    chunks,
    provider,
    model,
    top_k=3
):
    """
    AI-powered reranking of retrieved chunks.

    Returns the most relevant chunks.
    """

    logger.info(
        f"Reranking Started | Provider={provider}"
    )

    if not chunks:
        return []

    ranked = []

    for item in chunks:

        prompt = f"""
You are a Senior Software Engineer.

Rate how relevant the following repository chunk is
for answering the user's question.

Question:
{question}

Repository Chunk:

{item["chunk"]}

Return ONLY a number between 0 and 100.
"""

        try:

            # OpenAI
            if provider == "OpenAI":

                response = client.chat.completions.create(

                    model=model,

                    messages=[

                        {
                            "role": "user",
                            "content": prompt
                        }

                    ]

                )

                score = (
                    response
                    .choices[0]
                    .message
                    .content
                    .strip()
                )

            # Ollama
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

                score = (
                    response
                    .json()
                    .get(
                        "response",
                        "0"
                    )
                    .strip()
                )

            try:

                score = float(score)

            except:

                score = 0.0

            ranked.append({

                "score": score,

                "chunk": item["chunk"],

                "source": item["source"],

                "search_type": item.get(
                    "search_type",
                    "Semantic"
                )

            })

        except Exception as e:

            logger.error(
                f"Reranker Error: {e}"
            )

            ranked.append(item)

    ranked.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    logger.info(
        f"Reranking Complete | "
        f"Top {top_k} Selected"
    )

    return ranked[:top_k]