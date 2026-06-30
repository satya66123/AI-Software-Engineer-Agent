from src.utils.llm import generate_response


def generate_summary(
    readme_content,
    provider,
    model
):

    prompt = f"""
    Summarize this GitHub project.

    README:

    {readme_content[:3000]}
    """

    return generate_response(
        prompt=prompt,
        provider=provider,
        model=model
    )