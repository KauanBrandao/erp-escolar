from typing import Optional

from pydantic import BaseModel, Field


class DisciplinaBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100, description="Ex: Matemática")
    codigo: str = Field(..., min_length=2, max_length=20, description="Ex: MAT01")
    carga_horaria: int = Field(..., gt=0, description="Carga horária anual em horas")
    turma_id: int
    
class DisciplinaCreate(DisciplinaBase):
    pass


class DisciplinaResponse(DisciplinaBase):
    id:int

    class Config:
        from_atributes = True

class DisciplinaUptade(BaseModel):
    nome: Optional[str] = None
    codigo: Optional[str] = None
    carga_horaria: Optional[int] = None
    turma_id: Optional[int] = None