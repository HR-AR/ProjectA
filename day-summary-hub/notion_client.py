import os
from typing import List

from notion_client import Client

from config import get_env


class NotionClient:
    def __init__(self) -> None:
        token = get_env("NOTION_TOKEN")
        self.database_id = get_env("NOTION_DATABASE_ID")
        self.client = Client(auth=token)

    def save_day(self, narrative: str, tasks: List[str], classified: dict) -> None:
        # TODO: save to Notion database
        pass
