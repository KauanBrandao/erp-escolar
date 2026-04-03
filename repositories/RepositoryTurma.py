from pydantic import BaseModel, Field
from typing  import Optional

class RepositoryTurmaBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=50, description="Ex: 1 Ano A")
    serie: str = Field(..., min_length=2, max_length=50, description="Ex: 1 Ano")
    turno: str = Field(..., description="Matutino, vespertino ou noturno")
    ano_letivo: str = Field(..., ge=2000, le=2100)
    ativo = bool = True
    professor_id: Optional[int] = None

class RepositoryTurmaCreate(RepositoryTurmaBase):
    pass

class RepositoruTurmaResponse(RepositoryTurmaBase):
    id:int

    class Config:
        from_attribute = True

class RepositoruTurmaUpdade(BaseModel):
    nome: Optional[str] = None
    serie: Optional[str] = None
    turno: Optional[str] = None
    ano_letivo: Optional[int] = None
    ativo: Optional[bool] = None
    professor_id: Optional[bool] = None

