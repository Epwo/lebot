import requests


class Qbitorrent:
    def __init__(self, BaseUrl, password):
        self.BaseUrl = BaseUrl
        self.password = password
        self.cookie = "pending"

    def authenticate(self):
        url = f"{self.BaseUrl}/api/v2/auth/login"
        data = {"username": "admin", "password": self.password}
        response = requests.post(url, data=data)
        self.cookie = response.headers["Set-Cookie"].split(";")[0]
        return response.status_code

    def get_torrents(self):
        url = f"{self.BaseUrl}/api/v2/torrents/info"
        headers = {"Cookie": self.cookie}
        response = requests.get(url, headers=headers)
        return response.json()

    def add_torrent(self, magnet):
        url = f"{self.BaseUrl}/api/v2/torrents/add"
        headers = {"Cookie": self.cookie}
        data = {"urls": magnet}
        response = requests.post(url, headers=headers, data=data)
        return response
