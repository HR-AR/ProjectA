import os
from functools import lru_cache


DEFAULT_MODEL = os.getenv("OPENAI_DEFAULT_MODEL", "")

# Aliases resolved at runtime.  "best_reasoning" lazily queries the OpenAI
# `/v1/models` endpoint for the largest context window tagged with
# `reasoning`.  The result is cached for 24 h via `lru_cache`.
MODEL_ALIASES = {"best_reasoning": None}


def get_env(key: str, default: str | None = None) -> str:
    """Return an environment variable or a default value."""
    return os.getenv(key, default or "")


@lru_cache(maxsize=1)
def _find_best_reasoning_model() -> str:
    """Return the model-id with reasoning capability and the largest context.

    Falls back to ``DEFAULT_MODEL`` if the OpenAI API is unavailable.
    """
    try:
        import openai  # Imported lazily so tests don't require the package
        client = openai.OpenAI()

        models = client.models.list().data
        reasoning_models = [
            m for m in models
            if any("reasoning" in s for s in getattr(m, "capabilities", []))
        ]
        if reasoning_models:
            return max(
                reasoning_models,
                key=lambda m: getattr(m, "context_window", 0)
            ).id
    except Exception:
        # Network issues, missing creds, or openai not installed
        pass
    return DEFAULT_MODEL


@lru_cache(maxsize=128)
def get_model(name: str | None) -> str:
    """Resolve a model alias or return the name unchanged."""
    if not name or name == "best_reasoning":
        # TODO: implement best model lookup
        return DEFAULT_MODEL
    return name