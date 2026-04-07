from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import date

class RepositoryNotaBase(BaseModel):
    valor: Decimal = Field(..., ge=Decimal("0.0"), le=Decimal("10.0"), decimal_places=2)
    tipo: str = Field(..., description="trabalho ou prova")
    bimestre: int = Field(..., ge=1, le=4)
    lancado_em:date
    aluno_id: int
    disciplina_id:int

class RepositoryNotaCreate(RepositoryNotaBase):
    pass

class RepositoryNotaResponse(RepositoryNotaBase):
    id:int

    class config:
        from_attributes = True

class RepositoryNotaUpdate(BaseModel):
    valor: Optional[Decimal] = Field(None, ge=Decimal("0.0"), le=Decimal("10.0"), decimal_places=2)
    tipo: Optional[str] = None
    bimestre: Optional[int] = Field(None, ge=1, le=4)
    lancado_em: Optional[date] = None
