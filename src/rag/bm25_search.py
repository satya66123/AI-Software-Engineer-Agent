from rank_bm25 import BM25Okapi

from src.rag.vector_store import get_all_vectors
from src.utils.logger import logger


def bm25_search(
    question,
    provider,
    top_k=5
):
    """
    Keyword-based repository search using BM25.
    """

    logger.info(
        f"BM25 Search Started | Provider={provider}"
    )

    vectors = get_all_vectors(
        provider
    )

    if not vectors:

        logger.warning(
            "No vectors available for BM25 search."
        )

        return []

    corpus = []

    for item in vectors:

        corpus.append(
            item.get(
                "chunk",
                ""
            ).split()
        )

    bm25 = BM25Okapi(
        corpus
    )

    query = question.split()

    scores = bm25.get_scores(
        query
    )

    results = []

    for score, item in zip(
        scores,
        vectors
    ):

        results.append({

            "score": float(score),

            "chunk": item.get(
                "chunk",
                ""
            ),

            "source": item.get(
                "source",
                "Unknown"
            ),

            "search_type": "BM25"

        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    logger.info(
        f"BM25 Retrieved {len(results[:top_k])} chunks"
    )

    return results[:top_k]