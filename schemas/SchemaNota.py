from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class NotaBase(BaseModel):
    valor: Decimal = Field(..., ge=Decimal("0.0"), le=Decimal("10.0"), decimal_places=2)
    tipo: str = Field(..., description="trabalho ou prova")
    bimestre: int = Field(..., ge=1, le=4)
    disciplina_id:int

class NotaCreate(NotaBase):
    pass

class NotaResponse(NotaBase):
    id:int
    lancado_em:date

    class Config:
        from_attributes = True

class NotaUpdate(BaseModel):
    valor: Optional[Decimal] = Field(None, ge=Decimal("0.0"), le=Decimal("10.0"), decimal_places=2)
    tipo: Optional[str] = None
    bimestre: Optional[int] = Field(None, ge=1, le=4)
