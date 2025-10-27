from config import settings
from base_http_client import BaseHTTPClient
import requests
import logging

logger = logging.getLogger(__name__)


class CloudflareLLM(BaseHTTPClient):
    def __init__(self, token: str | None = None):
        token = token or settings.cloudflare_token
        self.account_id = settings.cloudflare_account_id
        self.model = settings.cloudflare_model
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{self.model}"

        super().__init__(token, url)

    def get_solution(self, task_text: str) -> str:
        payload = {
            "messages": [
                {"role": "system", "content": "You are a friendly assistant"},
                {"role": "user", "content": f"Объясни, как решить эту задачу:\n{task_text}"}
            ]
        }
        data = self.post(self.url, payload)

        result = (
                data.get("result", {}).get("response")
                or data.get("choices", [{}])[0].get("message", {}).get("content")
        )
        if not result:
            raise ValueError("Cloudflare API вернул пустой/неожиданный ответ")
        return result
