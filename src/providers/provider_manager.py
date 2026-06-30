from src.providers.ollama_provider import (
    generate_ollama
)

from src.providers.openai_provider import (
    generate_openai
)


def generate_response(
    provider,
    prompt,
    model
):

    if provider == "OpenAI":

        return generate_openai(
            prompt,
            model
        )

    return generate_ollama(
        prompt,
        model
    )