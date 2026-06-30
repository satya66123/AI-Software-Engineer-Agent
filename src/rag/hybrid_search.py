from src.rag.search import search_repository
from src.rag.bm25_search import bm25_search

from src.utils.logger import logger


def hybrid_search(
    question,
    provider,
    embedding_model,
    top_k=5
):
    """
    Hybrid Search

    Combines Semantic Search +
    BM25 Keyword Search.
    """

    logger.info(
        f"Hybrid Search Started | Provider={provider}"
    )

    semantic = search_repository(

        question=question,

        provider=provider,

        embedding_model=embedding_model,

        top_k=top_k

    )

    keyword = bm25_search(

        question=question,

        provider=provider,

        top_k=top_k

    )

    merged = {}

    for item in semantic:

        key = (
            item["source"],
            item["chunk"]
        )

        item["search_type"] = "Semantic"

        merged[key] = item

    for item in keyword:

        key = (
            item["source"],
            item["chunk"]
        )

        if key not in merged:

            merged[key] = item

        else:

            merged[key]["score"] = max(

                merged[key]["score"],

                item["score"]

            )

            merged[key]["search_type"] = "Hybrid"

    results = list(
        merged.values()
    )

    results.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    logger.info(
        f"Hybrid Search Retrieved "
        f"{len(results[:top_k])} chunks"
    )

    return results[:top_k]