import os
from typing import List, Tuple
from tenacity import retry, stop_after_attempt, wait_random_exponential

from config import get_model


def split_into_chunks(text: str, max_tokens: int = 1000) -> List[str]:
    # TODO: token aware splitting using tiktoken
    lines = text.splitlines()
    return ['\n'.join(lines[i:i + 50]) for i in range(0, len(lines), 50)]


@retry(reraise=True, stop=stop_after_attempt(6), wait=wait_random_exponential(multiplier=2))
def chat_with_retry(client, **kwargs):
    """Call OpenAI chat completions with automatic retries."""
    import openai  # Avoid mandatory dependency during testing
    return client.chat.completions.create(**kwargs)


def summarise(transcript: str, model: str, max_retries: int) -> Tuple[str, List[str]]:
    """Summarise a transcript and extract tasks using the given OpenAI model."""
    import openai  # Lazy import

    chunks = split_into_chunks(transcript)
    summaries = []
    client = openai.Client()

    for chunk in chunks:
        resp = chat_with_retry(client=client, model=model,
                               messages=[{"role": "user", "content": chunk}],
                               max_retries=max_retries, temperature=0.3, top_p=1, seed=123)
        summaries.append(resp.choices[0].message.content)

    final_summary = "\n".join(summaries)
    # TODO: combine summaries map-reduce style
    tasks = []
    return final_summary, tasks


def classify(tasks: List[str]) -> dict:
    return {"business": [t for t in tasks if "[Business]" in t],
            "personal": [t for t in tasks if "[Personal]" in t]}


def find_best_model() -> str:
    # TODO: call /v1/models and cache for 24h
    return get_model(os.getenv("OPENAI_DEFAULT_MODEL", ""))