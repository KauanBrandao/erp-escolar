from datetime import date
from typing import Optional

from pydantic import BaseModel


class MensalidadeBase(BaseModel):
    mes: int
    ano: int
    valor: float
    aluno_id: int

class MensalidadeCreate(MensalidadeBase):
    pass

class MensalidadeResponse(MensalidadeBase):
    id: int
    vencimento: date
    status: str

    class Config:
        from_attributes = True

class MensalidadeUpdate(BaseModel):
    aluno_id: Optional[int] = None
    mes: Optional[int] = None
    ano: Optional[int] = None
    valor: Optional[float] = None
