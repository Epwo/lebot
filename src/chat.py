import requests
from dotenv import load_dotenv
import os

# WhatsApp API Credentials
load_dotenv()
ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("META_PHONE_NUMBER_ID")
RECIPIENT_PHONE = "+33768384142"

# API Endpoint
url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"

# Custom Message Data
payload = {
    "messaging_product": "whatsapp",
    "to": RECIPIENT_PHONE,
    "text": {"body": "ca va ou quoi bel homme"},
}

# Headers
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

# Send Message
response = requests.post(url, json=payload, headers=headers)

# Print Response
print(response.json())
