from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class FrequenciaBase(BaseModel):
    data_aula: date
    presente: bool
    justificativa: Optional[str] = Field(None, description="Motivo da ausência, se houver")
    disciplina_id: int
    aluno_id: int


class FrequenciaCreate(FrequenciaBase):
    pass


class FrequenciaResponse(FrequenciaBase):
    id: int

    class Config:
        from_attributes = True


class FrequenciaUpdate(BaseModel):
    presente: Optional[bool] = None
    justificativa: Optional[str] = None