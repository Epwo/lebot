from src.api import LeBot
from dotenv import load_dotenv
import os
import src.reqs.ProwlarrClient as ProwlarrClient
import src.reqs.QbitorrentClient as QbitorrentClient
import json

load_dotenv()
MISTRAL_ACCESS_TOKEN = os.getenv("MISTRAL_API_KEY")
LeBot = LeBot(MISTRAL_ACCESS_TOKEN)

BASE_URL = os.getenv("BASE_URL")
RADARR_API_KEY = os.getenv("RADARR_API_KEY")
PROWLARR_API_KEY = os.getenv("PROWLARR_API_KEY")
RADARR_URL = f"https://radarr.{BASE_URL}"
PROWLARR_URL = f"https://prowlarr.{BASE_URL}"
QBITTORRENT_URL = f"https://qbittorrent.{BASE_URL}"

# print(LeBot.chat_with_lebot("What is the capital of France?"))
tools = open("src/clients.yaml", "r").read()
response = LeBot.is_humanity_Question(
    "Combien de temps il reste au telechargement de mon film?", tools
)
response = response.strip("```json")[1:-1]
is_humanity_question = json.loads(response)
print("--------")
print(is_humanity_question)
print("--------")

qbit = QbitorrentClient.Qbitorrent(BaseUrl=QBITTORRENT_URL, password="qbitorrent")
function_name = is_humanity_question["function"]
if hasattr(qbit, function_name):
    function = getattr(qbit, function_name)
    if is_humanity_question["args"]:
        result = function(**is_humanity_question["args"])
    else:
        result = function()
    print(result)
else:
    print(f"Function {function_name} not found in qbit")
