from fastapi import FastAPI, Request, Query
import uvicorn
import os
import requests
import json
import time
from src.api import LeBot

from src.reqs.ProwlarrClient import Prowlarr
from src.reqs.RadarrClient import Radarr

# from src.reqs.SonarrClient import Sonarr
from src.reqs.QbitorrentClient import Qbitorrent

from dotenv import load_dotenv

app = FastAPI()

load_dotenv()
VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("META_PHONE_NUMBER_ID")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

BASE_URL = os.getenv("BASE_URL")
RADARR_API_KEY = os.getenv("RADARR_API_KEY")
PROWLARR_API_KEY = os.getenv("PROWLARR_API_KEY")
RADARR_URL = f"https://radarr.{BASE_URL}"
PROWLARR_URL = f"https://prowlarr.{BASE_URL}"
QBITTORRENT_URL = f"https://qbittorrent.{BASE_URL}"
QBITTORRENT_PASSWORD = os.getenv("QBITTORRENT_PASSWORD")

WHATSAPP_API_URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

last_conversations = {}
recent_conversations = {}

LeBot = LeBot(MISTRAL_API_KEY)
tools = open("src/clients.yaml", "r").read()


@app.get("/webhook")  # ✅ Handle GET requests for Meta verification
async def verify_webhook(request: Request):
    params = request.query_params  # ✅ Extract all query parameters
    hub_mode = params.get("hub.mode")
    hub_challenge = params.get("hub.challenge")
    hub_verify_token = params.get("hub.verify_token")

    print(
        f"hub_mode: {hub_mode}, hub_challenge: {hub_challenge}, hub_verify_token: {hub_verify_token}"
    )

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        print(hub_challenge)
        return int(hub_challenge)  # ✅ Meta requires you to return this
    return {"error": "Invalid verification token"}


# Webhook endpoint to receive messages
@app.post("/webhook")
async def receive_message(request: Request):
    content = await request.json()
    try:
        user_name = (
            content.get("entry")[0]
            .get("changes")[0]
            .get("value")
            .get("contacts")[0]
            .get("profile")
            .get("name")
        )
        if user_name not in last_conversations.keys():
            last_conversations[user_name] = []
            print("new user !!")
        messages = (
            content.get("entry")[0].get("changes")[0].get("value").get("messages")[0]
        )
        if messages:
            sender_id = messages.get("from")
            msg = messages.get("text").get("body")
            print("msg:", msg)
            response = LeBot.is_humanity_Question(msg, tools)
            response = response.strip("```json")[1:-1]
            is_humanity_question = json.loads(response)
            time.sleep(2)
            # to avoid rate limiting, we wait for 1 second (due to the free tier)
            if is_humanity_question["answer"] == "human":
                # this is a humanly question lets just answer using the bot
                response = LeBot.chat_with_lebot(msg, last_conversations[user_name])
                last_conversations[user_name].append({"user": msg, "bot": response})
                send_whatsapp_message(sender_id, response)
            else:
                # this is a question that can be answered using one of the tools
                # lets make the request, and send the response
                req_resp = make_request(is_humanity_question, msg)
                response = LeBot.chat_with_lebot(
                    msg, last_conversations[user_name], req_resp
                )
                last_conversations[user_name].append({"user": msg, "bot": response})
                send_whatsapp_message(sender_id, response)

    except Exception as e:
        print(content)
        print(e)

    for user in last_conversations:
        last_conversations[user] = last_conversations[user][-5:]

    return {"status": "received"}


def send_whatsapp_message(recipient_id, message_text):
    """Send a WhatsApp message using Meta API"""
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "text": {"body": message_text},
    }

    response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)

    print("WhatsApp API Response:", response.json())  # Debugging
    return response.json()


def make_request(is_humanity_question, user_prompt):
    if is_humanity_question["tool_name"] == "Prowlarr":
        prowlarr = Prowlarr(PROWLARR_URL, PROWLARR_API_KEY)
        function_name = is_humanity_question["function"]
        if hasattr(prowlarr, function_name):
            function = getattr(prowlarr, function_name)
            response = function(**is_humanity_question["args"])
    elif is_humanity_question["tool_name"] == "Radarr":
        radarr = Radarr()
    elif is_humanity_question["tool_name"] == "Qbitorrent":
        qbit = Qbitorrent(BaseUrl=QBITTORRENT_URL, password=QBITTORRENT_PASSWORD)
        function_name = is_humanity_question["function"]
        if hasattr(qbit, function_name):
            function = getattr(qbit, function_name)
            if is_humanity_question["args"]:
                response = function(**is_humanity_question["args"])
            else:
                response = function()
    else:
        response = {"error": "Tool not found"}
    return response


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
