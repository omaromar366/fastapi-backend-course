import json
from base_http_client import BaseHTTPClient
from config import settings


class GistStorage(BaseHTTPClient):
    def __init__(self, base_url: str, token: str):
        super().__init__(token, base_url)
        self.token = token or settings.github_token
        self.gist_id = settings.gist_id
        self.api_url = f"https://api.github.com/gists/{self.gist_id}"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github+json"
        }

    def load_data(self):
        data = self.get(self.api_url)
        file_info = data.get("files", {}).get("tasks.json")
        if not file_info:
            return []
        try:
            return json.loads(file_info["content"])
        except json.JSONDecodeError:
            return []

    def save_data(self, tasks):
        content = json.dumps(tasks, ensure_ascii=False, indent=2)
        payload = {"files": {"tasks.json": {"content": content}}}
        return self.patch(self.api_url, payload)


def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task.get("id", 0) for task in tasks) + 1
