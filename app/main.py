import json
import logging
from typing import Any
from fastapi import Body, FastAPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="WhatsApp -> Discord Bridge")

@app.get("/health")
def health() -> dict:
    """ Rota simples para verificar se o servidor está no ar. """
    return {"status": "ok"}

@app.post("/webhook")
async def webhook(
    data: dict[str, Any] = Body(
        ...,
        examples=[{"event": "teste", "payload": {}}],
    )
) -> dict:
    """ Recebe os eventos enviados pelo WAHA. """
    logger.info("Evento recebido: %s", data.get("event"))
    logger.info("Payload completo:\n%s", json.dumps(data, ensure_ascii=False, indent=2))
    return {"received": True}
