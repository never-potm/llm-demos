# 1) set up once
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

# AI Company CLI

Generate concise **summaries** or polished **brochures** about a company by collecting links/content and prompting an LLM (OpenAI or Ollama). Both commands share the same provider and output behavior.

---

## 📦 Commands at a glance

- **`ai_company_summary`** – short, factual overview (who they are, what they do, key products, customers, quick links).  
- **`ai_company_brochure`** – marketing‑style brochure in Markdown (benefits, features, proof points, CTA).

---

## ✅ Prerequisites

- **Python 3.10+**
- One provider configured:
  - **OpenAI**: `OPENAI_API_KEY`, `OPENAAI_MODEL_NAME`
  - **Ollama**: `OLLAMA_API`, `OLLAMA_MODEL`

> **Tip (Ollama):** set `OLLAMA_API=http://localhost:11434` (or `.../api`) — **not** `/api/chat` or `/api/generate`.

---

## 🔑 Environment variables

### OpenAI
```bash
export OPENAI_API_KEY="sk-***"
export OPENAAI_MODEL_NAME="gpt-4o-mini"   # example; use what you provision
```

### Ollama
```bash
export OLLAMA_API="http://localhost:11434"  # or http://localhost:11434/api
export OLLAMA_MODEL="llama3.2"              # e.g., llama3.1:8b-instruct-q4_K_M
```

---

## 🚀 Common CLI flags

- `--name <company-name>` *(required)*: Company display name.  
- `--url <company-home-url>` *(required)*: Homepage; used for link classification/context.  
- `--provider <openai|ollama>` *(required)*: Model backend.  
- `--stream <true|false>` *(optional, default: false)*: Stream tokens when supported.  
- `--language <lang|code>` *(optional, default: english)*: Output language; e.g., `english`, `spanish`, `es`, `hi`.  
- `--out <path>` *(optional)*: Output path (defaults to `./output/<name>-<cmd>.md`).

> The tool **overwrites** the output file (opens in `"w"` mode).

---

## 🧠 Command: `ai_company_summary`

Produces a compact, factual summary suitable for briefings or internal notes.

### Example
```bash
python -m main ai_company_summary   --name Hugging Face   --url https://huggingface.co   --provider openai   --stream false   --language en
```

### Suggested outline (typical output)
- What the company does (1–2 lines)  
- Products/offerings (bullets)  
- Who uses it / credibility markers (logos, user counts)  
- Key links (About, Docs, Pricing, Careers)  
- One‑paragraph TL;DR in the selected language

---

## 🧾 Command: `ai_company_brochure`

Creates a concise, marketing‑oriented brochure in Markdown for external sharing.

### Example
```bash
python -m main ai_company_brochure   --name Huggingface   --url https://huggingface.co   --provider openai   --stream false   --language spanish
```

### Suggested outline (typical output)
- Title & subtitle  
- Value proposition (3–5 bullets)  
- Features/Capabilities (bullets) across modalities/use‑cases  
- Proof (customers, community stats, open‑source projects)  
- Call‑to‑action with relevant links (Docs, Pricing, Contact/Careers)

---

## 📝 Output

- Markdown file saved to `--out` (or default: `./output/<company>-<command>.md`)  
- The file is **truncated/overwritten** each run.  
- If you previously saw `FileExistsError`, it’s fixed by using `"w"` mode.

---

## 🛠 Provider behavior

- **OpenAIProvider**
  - `generate(prompt: str)` → single user message.
  - `chat(messages|str, system=None)` → role messages (system+user).
  - Streaming concatenates deltas.

- **OllamaProvider**
  - `generate(prompt: str)` → POST `/api/generate` with string `prompt`.
  - `chat(messages|str, system=None)` → POST `/api/chat` with list `messages`.
  - Ensure `OLLAMA_API` points to **root** (not `/api/chat` or `/api/generate`).
  - If you get `500 "new model will fit in available VRAM in single GPU"` → VRAM/quantization issue:
    - Use smaller/quantized tag (e.g., `*:q4_K_M`), free VRAM (`nvidia-smi`), or low‑VRAM options.

---

## 🧪 Examples

### OpenAI – English summary
```bash
python -m main ai_company_summary   --name Hugging Face   --url https://huggingface.co   --provider openai   --stream false   --language en
```

### Ollama – English brochure, streaming
```bash
python -m main ai_company_brochure   --name Hugging Face   --url https://huggingface.co   --provider ollama   --stream true   --language en
```

### OpenAI – Spanish brochure with custom output path
```bash
python -m main ai_company_brochure   --name Huggingface   --url https://huggingface.co   --provider openai   --stream false   --language es   --out ./output/hf-brochure-es.md
```

---

## 🧯 Troubleshooting

- **404** like `.../api/chat/api/generate`  
  Set `OLLAMA_API=http://localhost:11434` (or `/api`), not an endpoint.

- **FileExistsError** on output  
  Confirm your version opens files with `"w"` (truncate) rather than `"x"`.

- **OpenAI: passing role messages to `generate()`**  
  `generate()` expects a **string**. Use `chat()` for role messages.

- **Ollama: VRAM 500 error**  
  Use smaller/quantized model, free VRAM, or run CPU‑only temporarily.

---

## 🔚 Exit codes

- `0` – Success  
- `1` – Missing/invalid arguments  
- `2` – Provider configuration error (API key/model)  
- `3` – Provider runtime error (HTTP 4xx/5xx, VRAM, etc.)

---

## 💡 Tips

- Prefer a **system** rule in `chat()` to enforce JSON or specific formats.  
- For reproducibility, lower temperature/enable deterministic settings.  
- Multilingual outputs: ensure prompts include explicit language instruction.

