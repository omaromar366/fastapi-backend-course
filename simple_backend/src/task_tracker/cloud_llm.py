from config import settings
from base_http_client import BaseHTTPClient



class CloudflareLLM(BaseHTTPClient):
    def __init__(self, token: str | None = None):
        # Берём токен из аргумента или из настроек
        token = token or settings.cloudflare_token
        self.account_id = settings.cloudflare_account_id
        self.model = settings.cloudflare_model
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{self.model}"

        # Заголовки сразу передаём в родителя
        super().__init__(token, url)

    def get_solution(self, task_text: str) -> str:
        payload = {
            "messages": [
                {"role": "system", "content": "You are a friendly assistant"},
                {"role": "user", "content": f"Объясни, как решить эту задачу:\n{task_text}"}
            ]
        }
        try:
            data = self.post(self.url, payload)
            return data.get("result", {}).get("response", "Нет ответа от LLM")
        except Exception as e:
            return f"Ошибка запроса к LLM: {e}"

    def load_data(self):
        return None

    def save_data(self, data):
        return None

