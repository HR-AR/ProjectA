import os  # kept in case future logic needs env vars
from typing import List

from notion_client import Client

from config import get_env


class NotionClient:
    """Minimal wrapper around :class:`notion_client.Client`."""

    def __init__(self) -> None:
        token = get_env("NOTION_TOKEN")
        self.database_id = get_env("NOTION_DATABASE_ID")
        self.client = Client(auth=token)

    def save_day(self, narrative: str, tasks: List[str], classified: dict) -> None:
        """Persist the summary and tasks to the configured Notion database.

        Currently a stub. Replace the body with real persistence logic when
        credentials and schema are finalised.
        """
        # TODO: save to Notion database
        pass