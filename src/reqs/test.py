from RadarrClient import Radarr
from ProwlarrClient import Prowlarr
from QbitorrentClient import Qbitorrent
from dotenv import load_dotenv
import os
import json

load_dotenv()


BASE_URL = os.getenv("BASE_URL")
RADARR_API_KEY = os.getenv("RADARR_API_KEY")
PROWLARR_API_KEY = os.getenv("PROWLARR_API_KEY")
RADARR_URL = f"https://radarr.{BASE_URL}"
PROWLARR_URL = f"https://prowlarr.{BASE_URL}"
QBITTORRENT_URL = f"https://qbittorrent.{BASE_URL}"
# radarr = Radarr(BaseUrl=RADARR_URL, api_key=RADARR_API_KEY)
prowlarr = Prowlarr(BaseUrl=PROWLARR_URL, api_key=PROWLARR_API_KEY)

qbit = Qbitorrent(BaseUrl=QBITTORRENT_URL, password="qbitorrent")
qbit.authenticate()
# print(qbit.get_torrents())

# magnet = "https://prowlarr.media.swagman.fr/4/download?apikey=0f8a246ac39d49ca8c68f5b5a494fe43&link=eUUyWGlZTUpzcFRrVnptN3NIekEyaHdPYWdiMU5Qa1QvVVgva051NHE2R3g1ZTNnVzNNRHhzYzgxRndCTU13a1YxNjVaSW5sRGhaOCtTS0ZxaDNUV3kwN1VzSFVOdktoeWpLWGhSRDZjT3laOEZtcG5zTlRqN3ZhTGRMd0Q0ODU&file=Un+p%E2%80%99tit+truc+en+plus+2024+FRENCH+WEBRIP+"
# print(qbit.add_torrent(magnet))
results = prowlarr.search("Harry Potter", type="movie")
print(results)
with open("search_results.json", "w+") as file:
    json.dump(results, file, indent=4)
