import requests

from config.config import OLLAMA_API, OLLAMA_MODEL


class OllamaProvider:
    def __init__(self):
        self.model = OLLAMA_MODEL

    def generate(self, prompt: str) -> str:
        headers = {"Content-Type": "application/json"}

        payload = {
            "model": self.model,
            "messages": prompt,
            "stream": False
        }

        response = requests.post(OLLAMA_API, json=payload, headers=headers)
        return response.json()['message']['content']
