from typing import Optional  # currently unused but left for future expansion

import requests

from config import get_env


class LimitlessClient:
    """Client for the hypothetical Limitless GraphQL API."""

    def __init__(self) -> None:
        self.token: str = get_env("LIMITLESS_API_TOKEN")
        self.base_url: str = "https://api.limitless.com"

    def get_transcript(self, date: str) -> str:
        """Return the transcript for ``date``.

        This demo implementation simply returns an empty string. Replace with the
        real API call using ``requests`` when credentials are available.
        """
        # TODO: implement real API call
        _ = date  # placeholder to silence linters until implemented
        return ""