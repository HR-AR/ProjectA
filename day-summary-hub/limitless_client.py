from typing import Optional

import requests

from config import get_env


class LimitlessClient:
    def __init__(self) -> None:
        self.token = get_env("LIMITLESS_API_TOKEN")
        self.base_url = "https://api.limitless.com"

    def get_transcript(self, date: str) -> str:
        # TODO: implement real API call
        return ""
