import json
import os
import time
from functools import lru_cache
from pathlib import Path


DEFAULT_MODEL = os.getenv("OPENAI_DEFAULT_MODEL", "")
MODEL_ALIASES = {"best_reasoning": None}
_CACHE_FILE = Path(".model_cache.json")


def get_env(key: str, default: str | None = None) -> str:
    return os.getenv(key, default or "")


def _query_best_model() -> str:
    try:
        import openai  # type: ignore
    except Exception:
        return DEFAULT_MODEL

    client = openai.OpenAI(api_key=get_env("OPENAI_API_KEY"))
    try:
        models = client.models.list().data
    except Exception:
        return DEFAULT_MODEL

    best = None
    for m in models:
        cid = getattr(m, "id", "")
        if "reasoning" in cid:
            if best is None:
                best = m
            else:
                cw = getattr(m, "context_window", 0) or 0
                best_cw = getattr(best, "context_window", 0) or 0
                if cw > best_cw:
                    best = m
    return getattr(best, "id", DEFAULT_MODEL)


@lru_cache(maxsize=1)
def find_best_model() -> str:
    if _CACHE_FILE.exists():
        try:
            data = json.loads(_CACHE_FILE.read_text())
            if time.time() - data.get("time", 0) < 86400:
                MODEL_ALIASES["best_reasoning"] = data["model"]
                return data["model"]
        except Exception:
            pass
    model = _query_best_model()
    try:
        _CACHE_FILE.write_text(json.dumps({"model": model, "time": time.time()}))
    except Exception:
        pass
    MODEL_ALIASES["best_reasoning"] = model
    return model


@lru_cache(maxsize=1)
def get_model(name: str | None) -> str:
    if not name:
        name = DEFAULT_MODEL
    if name == "best_reasoning":
        cached = MODEL_ALIASES.get("best_reasoning")
        if cached:
            return cached
        return find_best_model()
    return name
