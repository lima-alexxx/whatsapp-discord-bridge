import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
WHATSAPP_GROUP_ID = os.getenv("WHATSAPP_GROUP_ID")
TIMEZONE = os.getenv("TIMEZONE", "America/Sao_Paulo")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()