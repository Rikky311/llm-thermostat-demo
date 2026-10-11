
"""Test the local Llama 3.2 model through Ollama."""

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_ai(prompt):
    """Send a prompt to Ollama and return the model's response."""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()
        result = response.json()

        return result["response"]

    except requests.exceptions.RequestException as error:
        return (
            "Could not connect to Ollama. "
            "Check that Ollama is running and the llama3.2 model is available.\n"
            f"Details: {error}"
        )


if __name__ == "__main__":
    answer = ask_ai("Explain artificial intelligence in simple words.")
    print("\nAI Response:")
    print(answer)