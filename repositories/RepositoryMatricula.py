from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class RepositoryMatriculaBase(BaseModel):
    aluno_id: int
    turma_id: int
    data_matricula: date
    status: str = Field(default="ativa", description="ativa, trancada ou cancelada")
    observacao: Optional[str] = Field(None, max_length=250)

class RepositoryMatriculaCreate(RepositoryMatriculaBase):
    pass

class RepositoryMatriculaResponse(RepositoryMatriculaBase):
    id:int
    
    class Config:
        from_atributes = True

class RepositoruMatriculaUpdate(BaseModel):
    turma_id: Optional[int] = None
    status: Optional[str] = None
    observacao: Optional[str] = None