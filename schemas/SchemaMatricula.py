from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class MatriculaBase(BaseModel):
    aluno_id: int
    turma_id: int
    data_matricula: date
    status: str = Field(default="ativa", description="ativa, trancada ou cancelada")
    observacao: Optional[str] = Field(None, max_length=250)

class MatriculaCreate(MatriculaBase):
    pass

class MatriculaResponse(MatriculaBase):
    id:int
    
    class Config:
        from_atributes = True

class MatriculaUpdate(BaseModel):
    turma_id: Optional[int] = None
    status: Optional[str] = None
    observacao: Optional[str] = None