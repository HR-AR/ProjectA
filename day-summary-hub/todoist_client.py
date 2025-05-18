from todoist_api_python.api import TodoistAPI

from config import get_env


class TodoistClient:
    """Wrapper around :class:`TodoistAPI` with basic retry handling."""

    def __init__(self) -> None:
        token = get_env("TODOIST_API_TOKEN")
        self.api = TodoistAPI(token)

    def add_task(self, task: str) -> bool:
        """Return ``True`` on success, ``False`` on any failure."""
        try:
            self.api.add_task(task)
            return True
        except Exception:
            return False