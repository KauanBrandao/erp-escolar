from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class AlunoBase(BaseModel):
    nome: str
    cpf: str = Field(..., pattern=r"^\d{11,15}$")
    telefone: int
    matricula_numero: int
    ativo: bool = True
    data_nascimento: date

class AlunoCreate(AlunoBase):
    pass

class AlunoResponse(AlunoBase):
    id: int
    criado_em: date

    class Config:
        from_attributes = True

class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[int] = None
    ativo: Optional[bool] = None
