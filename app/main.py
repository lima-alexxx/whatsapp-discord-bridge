#import json
import logging
from typing import Any
from fastapi import Body, FastAPI, BackgroundTasks

from app.config import LOG_LEVEL, WHATSAPP_GROUP_ID
from app.discord_client import send_to_discord
from app.messages import format_for_discord, parse_group_message

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("bridge")

if not WHATSAPP_GROUP_ID:
    raise RuntimeError("WHATSAPP_GROUP_ID não definida no .env")

app = FastAPI(title="WhatsApp -> Discord Bridge")

def forward_to_discord(sender: str, content: str) -> None:
    """ Roda em segundo plano depois que o webhook já respondeu ao WAHA. """
    try:
        send_to_discord(content, username=sender)
        logger.info("Mensagem encaminhada (remetente: %s)", sender)
    except Exception:
        logger.exception("Falha ao enviar para o Discord")

@app.get("/health")
def health() -> dict:
    """ Rota simples para verificar se o servidor está no ar. """
    return {"status": "ok"}

@app.post("/webhook")
def webhook(
    background_tasks: BackgroundTasks,
    data: dict[str, Any] = Body(
        ...,
        examples=[{"event": "teste", "payload": {}}],
    )
) -> dict:
    logger.debug("Payload bruto: %s", data)
    
    msg = parse_group_message(data)
    if msg is None:
        logger.debug("Evento ignorado")
        return {"received": True, "forwarded": False}

    background_tasks.add_task(forward_to_discord, msg.sender, format_for_discord(msg))
    return {"received": True, "forwarded": True}
