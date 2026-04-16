from sqlalchemy.orm import Session

from models.ModelFrequencia import ModelFrequencia
from schemas.SchemaFrequencia import FrequenciaCreate, FrequenciaUpdate


class FrequenciaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, frequencia: FrequenciaCreate) -> ModelFrequencia:
        db_frequencia = ModelFrequencia(**frequencia.model_dump())
        self.db.add(db_frequencia)
        self.db.commit()
        self.db.refresh(db_frequencia)
        return db_frequencia

    def get_byID(self, frequencia_id: int) -> ModelFrequencia | None:
        return self.db.query(ModelFrequencia).filter(ModelFrequencia.id == frequencia_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelFrequencia]:
        return self.db.query(ModelFrequencia).offset(skip).limit(limit).all()

    def update(self, frequencia_id: int, dados: FrequenciaUpdate) -> ModelFrequencia | None:
        frequencia = self.get_byID(frequencia_id)
        if not frequencia:
            return None

        if dados.presente is not None:
            frequencia.presente = dados.presente
        if dados.justificativa is not None:
            frequencia.justificativa = dados.justificativa

        self.db.commit()
        self.db.refresh(frequencia)
        return frequencia

    def delete(self, frequencia_id: int) -> bool:
        frequencia = self.get_byID(frequencia_id)
        if not frequencia:
            return False
        self.db.delete(frequencia)
        self.db.commit()
        return True
