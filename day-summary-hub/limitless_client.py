from __future__ import annotations

import requests

from config import get_env


class LimitlessClient:
    def __init__(self) -> None:
        self.token = get_env("LIMITLESS_API_TOKEN")
        self.base_url = "https://api.limitless.com"

    def get_transcript(self, date: str) -> str:
        if not self.token:
            return ""
        url = f"{self.base_url}/lifelogs?date={date}"
        try:
            resp = requests.get(url, headers={"Authorization": f"Bearer {self.token}"}, timeout=10)
            resp.raise_for_status()
            return resp.text
        except Exception:
            return ""
