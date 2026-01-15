import os, time, random, requests

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise RuntimeError("GROQ_API_KEY not set")


def call_llm(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Output ONLY a numbered list."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 600,
        "seed": 42,
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    for _ in range(5):
        r = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        if r.status_code == 429:
            time.sleep(2 + random.random())

    raise RuntimeError("LLM failed")
