import requests


class MyAskAI:
    def __init__(self, api_key: str, id: str):
        self.api_key = api_key
        self.id = id
        self.base_url = "https://myaskai.com/api/1.1"

    def query(self, q: str):
        try:
            response = requests.post(
                f"{self.base_url}/wf/ask-ai-query",
                json={"id": self.id, "api_key": self.api_key, "query": q},
            )
            if response.status_code == 200:
                return response.json()
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def __str__(self):
        return f"MyAskAI instance with ID: {self.id}"
