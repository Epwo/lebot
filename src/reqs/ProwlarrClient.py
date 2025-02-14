import requests
import json


class Prowlarr:
    def __init__(self, BaseUrl, api_key):
        self.BaseUrl = BaseUrl
        self.api_key = api_key

    def search(self, query, type):
        url = f"{self.BaseUrl}/api/v1/search?query={query}&t={type}"
        headers = {"X-Api-Key": self.api_key, "t": type}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        results = response.json() if response.text else {}
        results.sort(key=lambda x: int(x.get("grabs", 0)), reverse=True)
        results = results[:25]
        return results
