import calendar
from datetime import date

from sqlalchemy.orm import Session

from models.ModelMensalidade import ModelMensalidade
from schemas.SchemaMensalidade import MensalidadeCreate, MensalidadeUpdate


class MensalidadeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, mensalidade: MensalidadeCreate) -> ModelMensalidade:
        dados = mensalidade.model_dump()
        ultimo_dia = calendar.monthrange(dados["ano"], dados["mes"])[1]
        vencimento = date(dados["ano"], dados["mes"], ultimo_dia)
        db_mensalidade = ModelMensalidade(**dados, vencimento=vencimento, status="ativa")
        self.db.add(db_mensalidade)
        self.db.commit()
        self.db.refresh(db_mensalidade)
        return db_mensalidade

    def get_byID(self, mensalidade_id: int) -> ModelMensalidade | None:
        return self.db.query(ModelMensalidade).filter(ModelMensalidade.id == mensalidade_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelMensalidade]:
        return self.db.query(ModelMensalidade).offset(skip).limit(limit).all()

    def update(self, mensalidade_id: int, dados: MensalidadeUpdate) -> ModelMensalidade | None:
        mensalidade = self.get_byID(mensalidade_id)
        if not mensalidade:
            return None

        if dados.aluno_id is not None:
            mensalidade.aluno_id = dados.aluno_id
        if dados.mes is not None:
            mensalidade.mes = dados.mes
        if dados.ano is not None:
            mensalidade.ano = dados.ano
        if dados.valor is not None:
            mensalidade.valor = dados.valor

        self.db.commit()
        self.db.refresh(mensalidade)
        return mensalidade

    def delete(self, mensalidade_id: int) -> bool:
        mensalidade = self.get_byID(mensalidade_id)
        if not mensalidade:
            return False
        self.db.delete(mensalidade)
        self.db.commit()
        return True
