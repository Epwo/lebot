import requests


class Radarr:
    def __init__(self, BaseUrl, api_key):
        self.BaseUrl = BaseUrl
        self.api_key = api_key

    def search_movie(self, query):
        url = f"{self.BaseUrl}/api/v3/movie/lookup?term={query}"
        headers = {"X-Api-Key": self.api_key}
        response = requests.get(url, headers=headers)
        return response.json()

    def get_missing_movies(self):
        url = f"{self.BaseUrl}/api/v3/wanted/missing?page=1&pageSize=10&monitored=true"
        headers = {"X-Api-Key": self.api_key, "Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        return response.json()

    def lookup_movie(self, term):
        url = f"{self.BaseUrl}/api/v3/movie/lookup?term={term}"
        headers = {"X-Api-Key": self.api_key, "Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        return response.json()

    def get_downloding_queue(self):
        url = f"{self.BaseUrl}/api/v3/queue"
        headers = {"X-Api-Key": self.api_key, "Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        return response.json()

    def get_movies(self):
        url = f"{self.BaseUrl}/api/v3/movie"
        headers = {"X-Api-Key": self.api_key, "Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        return response.json()
