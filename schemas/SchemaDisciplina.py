from typing import Optional

from pydantic import BaseModel


class DisciplinaBase(BaseModel):
    nome: str
    codigo: str
    carga_horaria: int
    turma_id: int

class DisciplinaCreate(DisciplinaBase):
    pass

class DisciplinaResponse(DisciplinaBase):
    id: int

    class Config:
        from_attributes = True

class DisciplinaUpdate(BaseModel):
    nome: Optional[str] = None
    codigo: Optional[str] = None
    carga_horaria: Optional[int] = None
    turma_id: Optional[int] = None
