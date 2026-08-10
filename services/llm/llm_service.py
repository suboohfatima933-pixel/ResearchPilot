import ollama

from config.settings import OLLAMA_MODEL


class LLMService:
    """Handles communication with the configured Ollama model."""

    def generate(self, prompt: str) -> str:
        """Generate a response from the configured Ollama model."""

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]