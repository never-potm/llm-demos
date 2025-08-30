import requests

from config.config import OLLAMA_API


class OllamaProvider:
    def __init__(self, model: str):
        self.model = model

    def generate(self, prompt: str) -> str:
        headers = {"Content-Type": "application/json"}

        payload = {
            "model": self.model,
            "messages": prompt,
            "stream": False
        }

        response = requests.post(OLLAMA_API, json=payload, headers=headers)
        return response.json()['message']['content']
