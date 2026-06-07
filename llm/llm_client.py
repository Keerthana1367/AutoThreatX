import os
import json
import time
import random
import requests
from typing import Final

# ==============================
# Configuration (explicit)
# ==============================

GROQ_URL: Final[str] = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME: Final[str] = "llama-3.1-8b-instant"

GROQ_API_KEY: Final[str | None] = os.getenv("GROQ_API_KEY")

_groq_key = GROQ_API_KEY
if not _groq_key:
    try:
        import streamlit as st
        _groq_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        pass

if not _groq_key:
    raise RuntimeError("GROQ_API_KEY is not set. Set it as an environment variable or in .streamlit/secrets.toml")

GROQ_API_KEY = _groq_key


# ==============================
# LLM Call Function
# ==============================

def call_llm(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a cybersecurity threat modeling engine. "
                    "Output ONLY what is explicitly requested. "
                    "Do NOT add explanations, headings, or formatting. "
                    "If asked for a list, output ONLY a numbered list."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 600
    }

    retries = 5

    for attempt in range(retries):
        response = requests.post(
            GROQ_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        # ✅ Success
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]

        # 🔁 Rate-limit handling
        if response.status_code == 429:
            wait_time = 2.0 + random.uniform(0.0, 1.0)
            print(f"[RATE LIMIT] Waiting {wait_time:.1f}s...")
            time.sleep(wait_time)
            continue

        # ❌ Other errors
        print("Groq error:", response.text)
        response.raise_for_status()

    raise RuntimeError("Groq API failed after multiple retries")
