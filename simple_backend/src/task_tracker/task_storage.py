import os
import json
import requests

class GistStorage:
    def __init__(self):
        self.token = os.getenv("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")
        self.gist_id = os.getenv("7f6e92305aba7d32df48719ab3479959")
        self.api_url = f"https://api.github.com/gists/7f6e92305aba7d32df48719ab3479959"
        self.headers = {
            "Authorization": f"token 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",
            "Accept": "application/vnd.github+json"
        }

    def load_data(self):
        response = requests.get(self.api_url, headers=self.headers)
        response.raise_for_status()
        gist_data = response.json()
        file_content = gist_data["files"]["tasks.json"]["content"]
        return json.loads(file_content)

    def save_data(self, tasks):
        """Сохранить обновлённый список задач в Gist"""
        updated_content = json.dumps(tasks, ensure_ascii=False, indent=2)
        payload = {"files": {"tasks.json": {"content": updated_content}}}
        response = requests.patch(self.api_url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()