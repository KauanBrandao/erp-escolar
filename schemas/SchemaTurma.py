from typing import Optional

from pydantic import BaseModel, Field


class TurmaBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=50, description="Ex: 1 Ano A")
    serie: str = Field(..., min_length=2, max_length=50, description="Ex: 1 Ano")
    turno: str = Field(..., description="Matutino, vespertino ou noturno")
    ano_letivo: int = Field(..., ge=2000, le=2100)
    perfil_id: Optional[int] = None

class TurmaCreate(TurmaBase):
    pass

class TurmaResponse(TurmaBase):
    id: int

    class Config:
        from_attributes = True

class TurmaUpdate(BaseModel):
    nome: Optional[str] = None
    serie: Optional[str] = None
    turno: Optional[str] = None
    ano_letivo: Optional[int] = None
    perfil_id: Optional[int] = None
