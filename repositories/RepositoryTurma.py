from sqlalchemy.orm import Session

from models.ModelTurma import ModelTurma
from schemas.SchemaTurma import TurmaCreate, TurmaUpdate


class TurmaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, turma: TurmaCreate) -> ModelTurma:
        db_turma = ModelTurma(**turma.model_dump())
        self.db.add(db_turma)
        self.db.commit()
        self.db.refresh(db_turma)
        return db_turma

    def get_byID(self, turma_id: int) -> ModelTurma | None:
        return self.db.query(ModelTurma).filter(ModelTurma.id == turma_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelTurma]:
        return self.db.query(ModelTurma).offset(skip).limit(limit).all()

    def update(self, turma_id: int, dados: TurmaUpdate) -> ModelTurma | None:
        turma = self.get_byID(turma_id)
        if not turma:
            return None

        if dados.nome is not None:
            turma.nome = dados.nome
        if dados.serie is not None:
            turma.serie = dados.serie
        if dados.turno is not None:
            turma.turno = dados.turno
        if dados.ano_letivo is not None:
            turma.ano_letivo = dados.ano_letivo
        if dados.perfil_id is not None:
            turma.perfil_id = dados.perfil_id

        self.db.commit()
        self.db.refresh(turma)
        return turma

    def delete(self, turma_id: int) -> bool:
        turma = self.get_byID(turma_id)
        if not turma:
            return False
        self.db.delete(turma)
        self.db.commit()
        return True
