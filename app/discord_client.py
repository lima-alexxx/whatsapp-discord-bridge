import os
import requests
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

MAX_CONTENT = 2000
MAX_USERNAME = 80

def send_to_discord(content: str, username: str = "WhatsApp Bridge") -> None:
    """Envia uma mensagem de texto para o canal via webhook."""
    if not WEBHOOK_URL:
        raise RuntimeError("DISCORD_WEBHOOK_URL não definida no .env")

    payload = {
        "content": content[:MAX_CONTENT],
        "username": username[:MAX_USERNAME],
        "allowed_mentions": {"parse": []},
        }
    
    response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    response.raise_for_status() # imprime o erro se tiver algum