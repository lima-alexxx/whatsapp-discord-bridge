from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from zoneinfo import ZoneInfo
import logging

from app.config import TIMEZONE, WHATSAPP_GROUP_ID

DISCORD_LIMIT = 2000
logger = logging.getLogger("bridge") # para debug

@dataclass
class IncomingMessage:
    sender: str
    text: str
    sent_at: datetime

def parse_group_message(event: dict[str, Any]) -> Optional[IncomingMessage]:
    """ Extrai só os campos do meu interesse do evento do WAHA.
        
        Retorna None quando a mensagem deve ser ignorada.
    """

    if event.get("event") != "message":
        logger.debug("Ignorado: evento %r", event.get("event")) # para debug
        return None

    payload = event.get("payload") or {}

    if payload.get("from") != WHATSAPP_GROUP_ID:
        return None # filtra status, conversas privadas e outros grupos
    if payload.get("hasMedia"):
        logger.debug("Ignorado: mensagem com mídia")
        return None # no momento só mensagens de texto serão transferidas

    text = (payload.get("body") or "").strip()
    if not text:
        logger.debug("Ignorado: corpo vazio")
        return None

    data = payload.get("_data") or {}
    sender = data.get("notifyName") or "Participante"

    tz = ZoneInfo(TIMEZONE)
    timestamp = payload.get("timestamp") # em segundos
    sent_at = datetime.fromtimestamp(timestamp, tz=tz) if timestamp else datetime.now(tz)

    return IncomingMessage(sender=sender, text=text, sent_at=sent_at)


def format_for_discord (msg: IncomingMessage) -> str:
    """ Monta o texto final respeitando o limite final de 2000 caracteres. """

    footer = f"\n-# 🕒 {msg.sent_at:%d/%m/%Y %H:%M}"
    max_text = DISCORD_LIMIT - len(footer)
    text = msg.text if len(msg.text) <= max_text else (msg.text[: max_text - 1] + "...")

    return text + footer