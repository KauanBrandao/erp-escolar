from datetime import date
from typing import Optional

from pydantic import BaseModel


class ProfessorBase(BaseModel):
    nome: str
    cpf: str
    email: str
    telefone: str
    especialidade: str
    ativo: bool = True


class ProfessorCreate(ProfessorBase):
    pass


class ProfessorResponse(ProfessorBase):
    id: int
    criado_em: date

    class Config:
        from_attributes = True


class ProfessorUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    especialidade: Optional[str] = None
    ativo: Optional[bool] = None
