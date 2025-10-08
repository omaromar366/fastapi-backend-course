import requests
import os
from dotenv import load_dotenv

load_dotenv()

class CloudflareLLM:
    def __init__(self):
        self.token = os.getenv("CLOUDFLARE_AUTH_TOKEN")
        self.account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.model = os.getenv("CLOUDFLARE_MODEL", "@hf/google/gemma-7b-it")

        if not self.token or not self.account_id:
            raise ValueError("Не заданы CLOUDFLARE_AUTH_TOKEN или CLOUDFLARE_ACCOUNT_ID")

        self.url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{self.model}"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get_solution(self, task_text: str) -> str:
        payload = {
            "messages": [
                {"role": "system", "content": "You are a friendly assistant"},
                {"role": "user", "content": f"Объясни, как решить эту задачу:\n{task_text}"}
            ]
        }

        try:
            response = requests.post(self.url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get("result", {}).get("response", "Нет ответа от LLM")
        except requests.exceptions.RequestException as e:
            return f"Ошибка при запросе к Cloudflare: {e}"

print(os.getenv("CLOUDFLARE_AUTH_TOKEN"))