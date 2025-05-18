import os
from functools import lru_cache


DEFAULT_MODEL = os.getenv("OPENAI_DEFAULT_MODEL", "")
# Aliases resolved at runtime. "best_reasoning" lazily queries the OpenAI
# `/v1/models` endpoint for the largest context window tagged with
# `reasoning`. The result is cached for 24h via `lru_cache`.
MODEL_ALIASES = {"best_reasoning": None}


def get_env(key: str, default: str | None = None) -> str:
    return os.getenv(key, default or "")


@lru_cache(maxsize=1)
def _find_best_reasoning_model() -> str:
    """Return the model id with reasoning capability and largest context.

    This function calls the OpenAI API if available. When the API cannot be
    reached, it falls back to ``DEFAULT_MODEL``.
    """
    try:
        import openai

        client = openai.OpenAI()
        models = client.models.list().data
        reasoning_models = [
            m for m in models if any("reasoning" in s for s in getattr(m, "capabilities", []))
        ]
        if reasoning_models:
            return max(reasoning_models, key=lambda m: getattr(m, "context_window", 0)).id
    except Exception:
        pass
    return DEFAULT_MODEL


@lru_cache(maxsize=128)
def get_model(name: str | None) -> str:
    if not name or name == "best_reasoning":
        return _find_best_reasoning_model()
    return name
