import requests
import json


class Prowlarr:
    def __init__(self, BaseUrl, api_key):
        self.BaseUrl = BaseUrl
        self.api_key = api_key

    def search_movie(self, query, type):
        url = f"{self.BaseUrl}/api/v1/search?query={query}&type={type}"
        headers = {"X-Api-Key": self.api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json() if response.text else {}
        with open("prowlarr_search.json", "w+") as file:
            json.dump(json_data, file, indent=4)
        return response.json()
