from typing import Optional

from config.config import OPENAI_API_KEY
from openai import OpenAI


class OpenAIProvider:
    def __init__(self, model: str):
        self.model = model
        key = OPENAI_API_KEY
        if not key:
            raise RuntimeError("OpenAI API key not set")
        self.client = OpenAI(api_key=key)

    def generate(self, messages: str) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return resp.choices[0].message.content or ""
