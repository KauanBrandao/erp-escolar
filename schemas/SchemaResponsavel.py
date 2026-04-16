from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ResponsavelBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    parentesco: int

class ResponsavelCreate(ResponsavelBase):
    cpf: str = Field(..., pattern=r"^\d{11,15}$")
    telefone: str = Field(..., pattern=r"^\+?\d{10,15}$")

class ResponsavelResponse(ResponsavelBase):
    id: int
    cpf: str
    telefone: str

    class Config:
        from_attributes = True

class ResponsavelUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    parentesco: Optional[int] = None
