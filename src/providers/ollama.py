import json
import requests
from typing import List, Dict, Union, Optional

from config.config import OLLAMA_API, OLLAMA_MODEL
from utils.common import _to_bool


def _api_root(ollama_api: str) -> str:
    """
    Accepts:
      - http://localhost:11434
      - http://localhost:11434/api
      - http://localhost:11434/api/chat
      - http://localhost:11434/api/generate
    Returns: http://localhost:11434/api
    """
    base = ollama_api.rstrip("/")
    if base.endswith("/api/chat") or base.endswith("/api/generate"):
        return base.rsplit("/", 1)[0]
    if base.endswith("/api"):
        return base
    return base + "/api"


class OllamaProvider:
    def __init__(self, stream: bool = False):
        self.model = OLLAMA_MODEL
        self.stream = _to_bool(stream)
        self.api_root = _api_root(OLLAMA_API)  # e.g., http://localhost:11434/api

    # ------- /api/generate (single-turn) -------
    def generate(self, prompt: str, options: Optional[dict] = None) -> str:
        if not isinstance(prompt, str):
            raise TypeError("generate(prompt) expects a string. Use chat() for role messages.")
        url = f"{self.api_root}/generate"
        payload = {"model": self.model, "prompt": prompt, "stream": self.stream}
        if options:
            payload["options"] = options
        return self._post(url, payload, prefer="response")

    # ------- /api/chat (multi-turn) -------
    def chat(
        self,
        messages: Union[str, List[Dict[str, str]]],
        system: Optional[str] = None,
        options: Optional[dict] = None,
    ) -> str:
        url = f"{self.api_root}/chat"
        msg_list: List[Dict[str, str]] = []
        if system:
            msg_list.append({"role": "system", "content": system})
        if isinstance(messages, str):
            msg_list.append({"role": "user", "content": messages})
        else:
            msg_list.extend(messages)

        payload = {"model": self.model, "messages": msg_list, "stream": self.stream}
        if options:
            payload["options"] = options
        return self._post(url, payload, prefer="message.content")

    # ------- internals -------
    def _post(self, url: str, payload: dict, *, prefer: str) -> str:
        headers = {"Content-Type": "application/json"}

        with requests.post(url, json=payload, headers=headers, stream=self.stream) as r:
            if r.status_code >= 400:
                try:
                    body = r.json()
                except Exception:
                    body = r.text
                raise RuntimeError(f"Ollama error {r.status_code}: {body}")

            if not self.stream:
                data = r.json()
                return self._extract(data, prefer).strip()

            # streaming
            chunks: List[str] = []
            for line in r.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                piece = self._extract(obj, prefer, allow_empty=True)
                if piece:
                    chunks.append(piece)
                if obj.get("done"):
                    break
            return "".join(chunks).strip()

    def _extract(self, data: dict, prefer: str, allow_empty: bool = False) -> str:
        if prefer == "response":  # /api/generate
            val = data.get("response")
            if isinstance(val, str):
                return val
        elif prefer == "message.content":  # /api/chat
            msg = data.get("message")
            if isinstance(msg, dict):
                content = msg.get("content")
                if isinstance(content, str):
                    return content
        # fallback during streaming
        delta = data.get("delta")
        if isinstance(delta, str):
            return delta
        return "" if allow_empty else ""