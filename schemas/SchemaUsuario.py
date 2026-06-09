from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class UsuarioBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    email: str
    ativo: bool = True
    perfil_id: int

class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=8)

class UsuarioResponse(UsuarioBase):
    id: int
    criado_em: date

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    ativo: Optional[bool] = None
    perfil_id: Optional[int] = None