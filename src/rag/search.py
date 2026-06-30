from src.rag.embeddings import create_embedding
from src.rag.vector_store import get_all_vectors
from src.rag.similarity import cosine_similarity
from src.utils.logger import logger


def search_repository(
    question,
    provider,
    embedding_model,
    top_k=3
):
    """
    Semantic repository search using vector embeddings.
    """

    logger.info(
        f"Semantic Search Started | Provider={provider}"
    )

    question_embedding = create_embedding(
        text=question,
        provider=provider,
        model=embedding_model
    )

    if not question_embedding:

        logger.warning(
            "Question embedding generation failed."
        )

        return []

    results = []

    vectors = get_all_vectors(
        provider
    )

    logger.info(
        f"Loaded {len(vectors)} vectors"
    )

    if not vectors:

        logger.warning(
            "No vectors found."
        )

        return []

    for item in vectors:

        try:

            embedding = item.get(
                "embedding",
                []
            )

            if len(question_embedding) != len(
                embedding
            ):

                logger.warning(
                    f"Embedding mismatch: "
                    f"{len(question_embedding)} "
                    f"vs "
                    f"{len(embedding)}"
                )

                continue

            score = cosine_similarity(
                question_embedding,
                embedding
            )

            results.append({

                "score": float(score),

                "chunk": item.get(
                    "chunk",
                    ""
                ),

                "source": item.get(
                    "source",
                    "Unknown"
                )

            })

        except Exception as e:

            logger.error(
                f"Search Error: {e}"
            )

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    logger.info(
        f"Semantic Search Complete | "
        f"Retrieved {len(results[:top_k])} chunks"
    )

    return results[:top_k]