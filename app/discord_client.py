import os
import requests
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_to_discord(content: str, username: str = "WhatsApp Bridge") -> None:
    """Envia uma mensagem de texto para o canal via webhook."""
    if not WEBHOOK_URL:
        raise RuntimeError("DISCORD_WEBHOOK_URL não definida no .env")

    payload = {"content": content, "username": username}
    response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    response.raise_for_status() # imprime o erro se tiver algum