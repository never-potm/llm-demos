from config.config import OPENAI_API_KEY, OPENAAI_MODEL_NAME
from openai import OpenAI
from utils.common import _to_bool


class OpenAIProvider:
    def __init__(self, stream: bool = False):
        self.model = OPENAAI_MODEL_NAME
        key = OPENAI_API_KEY
        if not key:
            raise RuntimeError("OpenAI API key not set")
        self.client = OpenAI(api_key=key)
        self.stream = _to_bool(stream)

    # ---------- /generate (single-turn, string prompt) ----------
    def generate(self, prompt: str) -> str:
        if not isinstance(prompt, str):
            raise TypeError("generate(prompt) expects a string. Use chat() for messages.")

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=self.stream,
        )
        return self._collect(resp)

    # ---------- /chat (multi-turn, role messages) ----------
    def chat(self, messages, system: str = None) -> str:
        msg_list = []
        if system:
            msg_list.append({"role": "system", "content": system})
        if isinstance(messages, str):
            msg_list.append({"role": "user", "content": messages})
        else:
            msg_list.extend(messages)

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=msg_list,
            stream=self.stream,
        )
        return self._collect(resp)

    # ---------- internals ----------
    def _collect(self, resp) -> str:
        if not self.stream:
            text = resp.choices[0].message.content or ""
            return self._clean(text)

        # streaming
        out = []
        for chunk in resp:
            delta = chunk.choices[0].delta.content
            if delta:
                out.append(delta)
        return self._clean("".join(out))

    def _clean(self, text: str) -> str:
        # remove markdown fences if model includes them
        return text.replace("``", "").replace("markdown", "").strip()