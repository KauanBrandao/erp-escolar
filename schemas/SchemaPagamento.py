from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


# 1. Campos Base
class PagamentoBase(BaseModel):
    data_pagamento: date
    valor_pago: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    forma_pagamento: str = Field(..., min_length=3, max_length=50)
    comprovante: Optional[str] = None
    mensalidade_id: int

# 2. Schema para Criação (POST)
class PagamentoCreate(PagamentoBase):
    pass

# 3. Schema para Resposta (GET)
class PagamentoResponse(PagamentoBase):
    id: int

    class Config:
        from_attributes = True

# 4. Schema para Atualização (PATCH)
class PagamentoUpdate(BaseModel):
    data_pagamento: Optional[date] = None
    valor_pago: Optional[Decimal] = None
    forma_pagamento: Optional[str] = None
    comprovante: Optional[str] = None