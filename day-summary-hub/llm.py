from __future__ import annotations

import re
from typing import List, Tuple

from tenacity import retry, stop_after_attempt, wait_random_exponential

from config import get_env, get_model

try:
    import streamlit as st
except Exception:  # pragma: no cover - streamlit optional for tests
    class _Dummy:
        def __getattr__(self, name):
            return lambda *a, **k: None
    st = _Dummy()  # type: ignore


def _openai_client():
    try:
        import openai  # type: ignore
    except Exception as exc:  # pragma: no cover - openai optional for tests
        raise RuntimeError("openai package required") from exc
    return openai.OpenAI(api_key=get_env("OPENAI_API_KEY"))


@retry(reraise=True, stop=stop_after_attempt(6), wait=wait_random_exponential(multiplier=2))
def chat_with_retry(**kwargs):
    client = _openai_client()
    st.logger.info("Calling OpenAI")
    return client.chat.completions.create(**kwargs)


def split_into_chunks(text: str, max_tokens: int = 1000) -> List[str]:
    words = text.split()
    chunks: List[str] = []
    current: List[str] = []
    for word in words:
        current.append(word)
        if len(current) >= max_tokens:
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))
    return chunks


def summarise(transcript: str, model: str, max_retries: int) -> Tuple[str, List[str]]:
    chunks = split_into_chunks(transcript, 1000)
    st.logger.info("Summarising %d chunks", len(chunks))
    summaries = []
    for chunk in chunks:
        resp = chat_with_retry(
            model=model,
            messages=[{"role": "user", "content": chunk}],
            temperature=0.3,
            top_p=1,
            seed=123,
            max_retries=max_retries,
        )
        summaries.append(resp.choices[0].message.content)
    combined = "\n".join(summaries)
    resp = chat_with_retry(
        model=model,
        messages=[{"role": "user", "content": combined}],
        temperature=0.3,
        top_p=1,
        seed=123,
        max_retries=max_retries,
    )
    final_summary = resp.choices[0].message.content
    tasks = re.findall(r"-\s*(.+\[.*?\])", final_summary)
    return final_summary, tasks


def classify(tasks: List[str]) -> dict:
    return {
        "business": [t for t in tasks if "[Business]" in t],
        "personal": [t for t in tasks if "[Personal]" in t],
    }


def find_best_model() -> str:
    from config import find_best_model as _find

    return _find()
