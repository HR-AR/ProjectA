import os
from typing import List, Tuple

from tenacity import retry, stop_after_attempt, wait_random_exponential

from config import get_model


def split_into_chunks(text: str, max_tokens: int = 1000) -> List[str]:
    """Token-aware splitting (via *tiktoken*) with a safe line-based fallback."""
    try:
        import tiktoken  # type: ignore

        enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
        tokens = enc.encode(text)
        chunks = [tokens[i : i + max_tokens] for i in range(0, len(tokens), max_tokens)]
        return [enc.decode(c) for c in chunks]
    except Exception:
        # Fallback if *tiktoken* isn’t available
        lines = text.splitlines()
        return ["\n".join(lines[i : i + 50]) for i in range(0, len(lines), 50)]


@retry(reraise=True, stop=stop_after_attempt(6), wait=wait_random_exponential(multiplier=2))
def chat_with_retry(client, **kwargs):
    """Call OpenAI chat completions with automatic retries."""
    import openai  # noqa: F401 – lazy import so tests can run without the pkg
    return client.chat.completions.create(**kwargs)


def summarise(transcript: str, model: str, max_retries: int) -> Tuple[str, List[str]]:
    """Summarise a transcript and extract tasks using the given OpenAI model."""
    import openai  # Lazy import to keep the top-level dependency optional

    chunks = split_into_chunks(transcript)
    summaries: List[str] = []
    client = openai.Client()

    for chunk in chunks:
        resp = chat_with_retry(
            client=client,
            model=model,
            messages=[{"role": "user", "content": chunk}],
            max_retries=max_retries,
            temperature=0.3,
            top_p=1,
            seed=123,
        )
        summaries.append(resp.choices[0].message.content)

    final_summary = "\n".join(summaries)
    # TODO: combine summaries map-reduce style
    tasks: List[str] = []
    return final_summary, tasks


def classify(tasks: List[str]) -> dict:
    return {
        "business": [t for t in tasks if "[Business]" in t],
        "personal": [t for t in tasks if "[Personal]" in t],
    }


def find_best_model() -> str:
    """Return the best reasoning model via :func:`config.get_model`."""
    return get_model("best_reasoning")