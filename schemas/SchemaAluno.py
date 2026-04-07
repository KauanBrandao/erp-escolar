from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

# Deixei os comentarios da Ia para facilitar o entendimento:

# 1. Schema Base: Campos que são comuns a todos
class AlunoBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    cpf: str = Field(..., pattern=r"^\d{11,15}$")
    telefone: int
    matricula_numero: int
    ativo: bool = True
    data_nascimento: date

# 2. Schema de Criação: O que o cliente envia (POST)
class AlunoCreate(AlunoBase):
    pass

# 3 Oque a API vai receber (GET)
class AlunoResponse(AlunoBase):
    id: int
    criado_em: date

    class config:
        # Permite converter o objeto do SQLAlchemy (ModelAluno) direto para este Schema
        from_attributes = True


# 4. Schema de Atualização: Todos os campos viram opcionais (PATCH/PUT)
class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[int] = None
    ativo: Optional[bool] = None