import os
from typing import List, Tuple

try:
    import openai  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    openai = None

from tenacity import retry, stop_after_attempt, wait_random_exponential

from config import get_model


def _default_client():
    if openai is None:
        raise ImportError("openai package is required")
    return getattr(openai, "OpenAI", openai)()


def split_into_chunks(text: str, max_tokens: int = 1000) -> List[str]:
    """Token-aware splitting (via *tiktoken*) with a safe line-based fallback."""
    try:
        import tiktoken  # type: ignore

        enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
        tokens = enc.encode(text)
        chunks = [tokens[i : i + max_tokens] for i in range(0, len(tokens), max_tokens)]
        return [enc.decode(c) for c in chunks]
    except Exception:
        # Fallback if *tiktoken* isn't available
        lines = text.splitlines()
        return ["\n".join(lines[i : i + 50]) for i in range(0, len(lines), 50)]


def _chat_request(client, **kwargs):
    if hasattr(client, "chat") and hasattr(client.chat, "completions"):
        return client.chat.completions.create(**kwargs)
    return client.ChatCompletion.create(**kwargs)


def chat_with_retry(*, client=None, max_attempts: int = 6, **kwargs):
    client = client or _default_client()

    @retry(reraise=True, stop=stop_after_attempt(max_attempts), wait=wait_random_exponential(multiplier=2))
    def _call():
        return _chat_request(client, **kwargs)

    return _call()


def summarise(transcript: str, model: str, max_retries: int, client=None) -> Tuple[str, List[str]]:
    """Summarise a transcript and extract tasks using the given OpenAI model."""
    chunks = split_into_chunks(transcript)
    summaries = []
    for chunk in chunks:
        resp = chat_with_retry(client=client, model=model,
                               messages=[{"role": "user", "content": chunk}],
                               max_attempts=max_retries,
                               temperature=0.3, top_p=1, seed=123)
        summaries.append(resp.choices[0].message.content)
    final_summary = "\n".join(summaries)
    # TODO: combine summaries map-reduce style
    tasks = []
    return final_summary, tasks


def classify(tasks: List[str]) -> dict:
    return {
        "business": [t for t in tasks if "[Business]" in t],
        "personal": [t for t in tasks if "[Personal]" in t],
    }


def find_best_model() -> str:
    """Return the best reasoning model via :func:`config.get_model`."""
    return get_model(os.getenv("OPENAI_DEFAULT_MODEL", ""))