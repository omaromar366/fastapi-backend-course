import json
from base_http_client import BaseHTTPClient
from config import settings
import logging

logger = logging.getLogger(__name__)


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
        try:
            data = self.get(self.api_url)
            file_info = data.get("files", {}).get("tasks.json")
            if not file_info:
                logger.warning("Файл tasks.json не найден в gist %s", self.gist_id)
                return []

            return json.loads(file_info["content"])

        except json.JSONDecodeError as e:
            logger.error("Ошибка парсинга JSON из tasks.json: %s", e)
            return []
        except Exception as e:
            logger.exception("Ошибка при загрузке данных из Gist: %s", e)
            return []

    def save_data(self, tasks: list):
        content = json.dumps(tasks, ensure_ascii=False, indent=2)
        payload = {"files": {"tasks.json": {"content": content}}}
        try:
            response = self.patch(self.api_url, payload)
            logger.info("Успешно сохранены данные в gist %s", self.gist_id)
            return response
        except Exception as e:
            logger.exception("Ошибка при сохранении данных в gist %s: %s", self.gist_id, e)
            raise


def get_next_id(tasks: list):
    if not tasks:
        return 1
    return max(task.get("id", 0) for task in tasks) + 1
