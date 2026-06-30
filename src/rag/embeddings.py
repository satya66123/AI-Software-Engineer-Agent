import os
import requests

from openai import OpenAI

from src.utils.logger import logger

logger.info("Embedding module loaded")

OLLAMA_URL = "http://localhost:11434/api/embeddings"

client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)


def create_embedding(
    text,
    provider="Ollama",
    model=None
):

    try:

        # OpenAI Embeddings
        if provider == "OpenAI":

            embedding_model = (
                model
                if model
                else "text-embedding-3-small"
            )

            response = (
                client.embeddings.create(
                    model=embedding_model,
                    input=text
                )
            )

            logger.info(
                "OpenAI embedding generated"
            )

            return (
                response
                .data[0]
                .embedding
            )

        # Ollama Embeddings
        embedding_model = (
            model
            if model
            else "nomic-embed-text"
        )

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": embedding_model,
                "prompt": text
            }
        )

        response.raise_for_status()

        embedding = response.json()[
            "embedding"
        ]

        logger.info(
            "Ollama embedding generated"
        )

        return embedding

    except Exception as e:

        logger.error(
            f"Embedding Error: {e}"
        )

        return []

