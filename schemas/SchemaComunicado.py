from datetime import date
from typing import Optional

from pydantic import BaseModel


class ComunicadoBase(BaseModel):
    titulo: str
    conteudo: str
    destinatario_id: int
    ativo: bool = True

class ComunicadoCreate(ComunicadoBase):
    pass

class ComunicadoResponse(ComunicadoBase):
    id: int
    enviado_em: date

    class Config:
        from_attributes = True

class ComunicadoUpdate(BaseModel):
    titulo: Optional[str] = None
    conteudo: Optional[str] = None
    ativo: Optional[bool] = None
