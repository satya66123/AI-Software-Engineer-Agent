import json
import os

OLLAMA_VECTOR_FILE = "data/ollama_vectors.json"
OPENAI_VECTOR_FILE = "data/openai_vectors.json"


def get_vector_file(provider):

    if provider == "OpenAI":
        return OPENAI_VECTOR_FILE

    return OLLAMA_VECTOR_FILE


def add_vector(
    chunk,
    embedding,
    source,
    provider
):

    vector_file = get_vector_file(
        provider
    )

    vectors = []

    if os.path.exists(
        vector_file
    ):

        with open(
            vector_file,
            "r",
            encoding="utf-8"
        ) as f:

            vectors = json.load(f)

    vectors.append({

        "chunk": chunk,

        "embedding": embedding,

        "source": source

    })

    with open(
        vector_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            vectors,
            f
        )


def get_all_vectors(
    provider
):

    vector_file = get_vector_file(
        provider
    )

    if not os.path.exists(
        vector_file
    ):
        return []

    with open(
        vector_file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def clear_vectors(
    provider
):

    vector_file = get_vector_file(
        provider
    )

    with open(
        vector_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            [],
            f
        )