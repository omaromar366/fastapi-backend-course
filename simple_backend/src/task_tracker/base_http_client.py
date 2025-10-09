import requests
from abc import ABC, abstractmethod


class BaseHTTPClient(ABC):
    def __init__(self, token: str, url: str):
        self.token = token
        self.url = url
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get(self, url: str):
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def patch(self, url: str, payload: dict):
        resp = requests.patch(url, headers=self.headers, json=payload)
        resp.raise_for_status()
        return resp.json()

    def post(self, url: str, payload: dict):
        resp = requests.post(url, headers=self.headers, json=payload)
        resp.raise_for_status()
        return resp.json()

