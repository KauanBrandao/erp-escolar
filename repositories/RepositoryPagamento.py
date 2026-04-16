from sqlalchemy.orm import Session

from models.ModelPagamento import ModelPagamento
from schemas.SchemaPagamento import PagamentoCreate, PagamentoUpdate


class PagamentoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, pagamento: PagamentoCreate) -> ModelPagamento:
        db_pagamento = ModelPagamento(**pagamento.model_dump())
        self.db.add(db_pagamento)
        self.db.commit()
        self.db.refresh(db_pagamento)
        return db_pagamento

    def get_byID(self, pagamento_id: int) -> ModelPagamento | None:
        return self.db.query(ModelPagamento).filter(ModelPagamento.id == pagamento_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelPagamento]:
        return self.db.query(ModelPagamento).offset(skip).limit(limit).all()

    def update(self, pagamento_id: int, dados: PagamentoUpdate) -> ModelPagamento | None:
        pagamento = self.get_byID(pagamento_id)
        if not pagamento:
            return None

        if dados.data_pagamento is not None:
            pagamento.data_pagamento = dados.data_pagamento
        if dados.valor_pago is not None:
            pagamento.valor_pago = dados.valor_pago
        if dados.forma_pagamento is not None:
            pagamento.forma_pagamento = dados.forma_pagamento
        if dados.comprovante is not None:
            pagamento.comprovante = dados.comprovante

        self.db.commit()
        self.db.refresh(pagamento)
        return pagamento

    def delete(self, pagamento_id: int) -> bool:
        pagamento = self.get_byID(pagamento_id)
        if not pagamento:
            return False
        self.db.delete(pagamento)
        self.db.commit()
        return True
