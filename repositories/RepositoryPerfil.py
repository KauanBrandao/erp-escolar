from typing import Optional

from pydantic import BaseModel, Field


class RepositoryPerfilBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100, description="Nome do perfil de acesso")
    descricao: Optional[str] = Field(None, max_length=250, description="Breve descrição das permissões")

class RepositoryPerfilCreate(RepositoryPerfilBase):
    pass 

class RepositoryPerfilResponse(RepositoryPerfilBase):
    id: int
    nome: str

    class config:
        from_atributtes = True

class RespositoryPerfilUpdate(BaseModel):
    nome: Optional[int] = None
    descricao: Optional[str] = None