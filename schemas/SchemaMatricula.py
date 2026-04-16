from datetime import date
from typing import Optional

from pydantic import BaseModel


class MatriculaBase(BaseModel):
    aluno_id: int
    turma_id: int
    data_matricula: date
    status: str = "ativa"
    observacao: Optional[str] = None

class MatriculaCreate(MatriculaBase):
    pass

class MatriculaResponse(MatriculaBase):
    id: int

    class Config:
        from_attributes = True

class MatriculaUpdate(BaseModel):
    turma_id: Optional[int] = None
    status: Optional[str] = None
    observacao: Optional[str] = None
