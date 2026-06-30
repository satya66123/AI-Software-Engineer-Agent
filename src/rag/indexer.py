from src.rag.chunker import chunk_text
from src.rag.embeddings import create_embedding
from src.rag.vector_store import add_vector

from src.utils.logger import logger


def build_repository_index(
    files,
    provider,
    model
):

    logger.info(
        f"Indexing Started | Provider={provider}"
    )
    logger.info(
        f"Indexing Started | Model={model}"
    )


    # Fixed Embedding Models

    embedding_model = (
        "text-embedding-3-small"
        if provider == "OpenAI"
        else "nomic-embed-text"
    )

    logger.info(
        f"Embedding Model: {embedding_model}"
    )

    total_chunks = 0

    for file in files:

        try:

            with open(
                file["path"],
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:

                content = f.read()

            if not content.strip():
                continue

            chunks = chunk_text(
                content
            )

            logger.info(
                f"{file['path']} -> "
                f"{len(chunks)} chunks"
            )

            for chunk in chunks:

                embedding = create_embedding(
                    text=chunk,
                    provider=provider,
                    model=embedding_model
                )

                if not embedding:
                    continue

                add_vector(
                    chunk=chunk,
                    embedding=embedding,
                    source=file["path"],
                    provider=provider
                )

                total_chunks += 1

        except Exception as e:

            logger.error(
                f"Index Error: {e}"
            )

    logger.info(
        f"Total Chunks Indexed: "
        f"{total_chunks}"
    )

    return total_chunks
