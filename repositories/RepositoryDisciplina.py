from pydantic import BaseModel, Field
from typing import Optional


class RepositoryDisciplinaBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100, description="Ex: Matemática")
    codigo: str = Field(..., min_length=2, max_length=20, description="Ex: MAT01")
    carga_horaria: int = Field(..., gt=0, description="Carga horária anual em horas")
    turma_id: int
    
class RepositoryDisciplinaCreate(RepositoryDisciplinaBase):
    pass


class RepositoryDisciplinaResponse(RepositoryDisciplinaBase):
    id:int

    class Config:
        from_atributes = True

class RepositoryDisciplinaUptade(BaseModel):
    nome: Optional[str] = None
    codigo: Optional[str] = None
    carga_horaria: Optional[int] = None
    turma_id: Optional[int] = None