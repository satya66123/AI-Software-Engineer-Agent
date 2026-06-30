import requests


def generate_ollama(
    prompt,
    model="qwen2.5:1.5b"
):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]