from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class RepositoryResponsavelBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    parentesco: int

class RepositoryResponsavelResponse(RepositoryResponsavelBase):
    cpf:str = Field(..., pattern=r"^\d{11,15}$")

class RepositoryResponsavelResponse(RepositoryResponsavelBase):
    id:int 
    telefone: int

    class config:
        from_atributtes = True

class RepositoryResponsavel(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    parentesco: Optional[int] = None