import ollama

from config.settings import OLLAMA_MODEL


class LLMService:
    """Handles communication with the configured Ollama model."""

    def generate(
        self,
        prompt: str,
        response_format=None,
    ) -> str:
        """Generate a response from the configured Ollama model."""

        if not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            format=response_format,
        )

        content = response["message"]["content"]

        if not content or not content.strip():
            raise ValueError(
                "The AI returned an empty response."
            )

        return content.strip()