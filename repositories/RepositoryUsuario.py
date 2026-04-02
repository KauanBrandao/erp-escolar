from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date


class RepositoryUsuarioBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    ativo: bool = True
    perfil_id: int

class RepositoryUsuarioCreate(RepositoryUsuarioBase):
    senha: str = Field(..., min_length=8)

class RepositoryUsuarioResponse(RepositoryUsuarioBase):
    id: int
    criado_em: date

    class config:
        from_atributtes = True

class RepositoryUsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    ativo: Optional[bool] = None
    perfil_id: Optional[int] = None