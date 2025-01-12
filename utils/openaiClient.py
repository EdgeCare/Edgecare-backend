import os
import openai
from dotenv import load_dotenv
from typing import Optional

load_dotenv()
class OpenAIClient:

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model

        if not self.api_key:
            raise ValueError("OpenAI API key is not configured. Set it as an environment variable or pass it explicitly.")

        openai.api_key = self.api_key
        openai.api_type = "openai"
        openai.api_version = None  # Default version

    def generate_response(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"Error during OpenAI API request: {e}")