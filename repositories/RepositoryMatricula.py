from sqlalchemy.orm import Session

from models.ModelMatricula import ModelMatricula
from schemas.SchemaMatricula import MatriculaCreate, MatriculaUpdate


class MatriculaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, matricula: MatriculaCreate) -> ModelMatricula:
        db_matricula = ModelMatricula(**matricula.model_dump())
        self.db.add(db_matricula)
        self.db.commit()
        self.db.refresh(db_matricula)
        return db_matricula

    def get_byID(self, matricula_id: int) -> ModelMatricula | None:
        return self.db.query(ModelMatricula).filter(ModelMatricula.id == matricula_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelMatricula]:
        return self.db.query(ModelMatricula).offset(skip).limit(limit).all()

    def update(self, matricula_id: int, dados: MatriculaUpdate) -> ModelMatricula | None:
        matricula = self.get_byID(matricula_id)
        if not matricula:
            return None

        if dados.turma_id is not None:
            matricula.turma_id = dados.turma_id
        if dados.status is not None:
            matricula.status = dados.status
        if dados.observacao is not None:
            matricula.observacao = dados.observacao

        self.db.commit()
        self.db.refresh(matricula)
        return matricula

    def delete(self, matricula_id: int) -> bool:
        matricula = self.get_byID(matricula_id)
        if not matricula:
            return False
        self.db.delete(matricula)
        self.db.commit()
        return True
