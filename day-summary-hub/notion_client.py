import datetime as dt
from typing import List

from notion_client import Client

from config import get_env


class NotionClient:
    def __init__(self) -> None:
        token = get_env("NOTION_TOKEN")
        self.database_id = get_env("NOTION_DATABASE_ID")
        self.client = Client(auth=token)

    def save_day(self, narrative: str, tasks: List[str], classified: dict) -> None:
        if not self.database_id:
            return
        properties = {
            "Date": {"date": {"start": dt.date.today().isoformat()}},
            "Narrative": {"rich_text": [{"text": {"content": narrative}}]},
            "Tasks": {"rich_text": [{"text": {"content": "\n".join(tasks)}}]},
        }
        self.client.pages.create(parent={"database_id": self.database_id}, properties=properties)
