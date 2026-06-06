import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("erp_escolar")


def registrar_log(usuario: str, acao: str):
    logger.info(f"[{usuario}] {acao}")
