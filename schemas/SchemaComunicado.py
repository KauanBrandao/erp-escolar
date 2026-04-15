from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


# 1. Campos Base
class ComunicadoBase(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=150)
    conteudo: str = Field(..., min_length=1)
    destinatario_id: int
    ativo: bool = True

# 2. Schema para Criação (POST)
class ComunicadoCreate(ComunicadoBase):
    # enviado_em pode ser omitido na criação para o banco gerar automaticamente
    pass

# 3. Schema para Resposta (GET)
class ComunicadoResponse(ComunicadoBase):
    id: int
    enviado_em: date

    class Config:
        from_attributes = True

# 4. Schema para Atualização (PATCH)
class ComunicadoUpdate(BaseModel):
    titulo: Optional[str] = None
    conteudo: Optional[str] = None
    ativo: Optional[bool] = None