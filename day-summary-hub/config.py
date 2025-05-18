import os
from functools import lru_cache


DEFAULT_MODEL = os.getenv("OPENAI_DEFAULT_MODEL", "")
MODEL_ALIASES = {"best_reasoning": None}


def get_env(key: str, default: str | None = None) -> str:
    return os.getenv(key, default or "")


@lru_cache(maxsize=1)
def get_model(name: str | None) -> str:
    if not name or name == "best_reasoning":
        # TODO: implement best model lookup
        return DEFAULT_MODEL
    return name
