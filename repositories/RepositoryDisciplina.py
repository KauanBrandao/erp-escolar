from sqlalchemy.orm import Session

from models.ModelDisciplina import ModelDisciplina
from schemas.SchemaDisciplina import DisciplinaCreate, DisciplinaUpdate


class DisciplinaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, disciplina: DisciplinaCreate) -> ModelDisciplina:
        db_disciplina = ModelDisciplina(**disciplina.model_dump())
        self.db.add(db_disciplina)
        self.db.commit()
        self.db.refresh(db_disciplina)
        return db_disciplina

    def get_byID(self, disciplina_id: int) -> ModelDisciplina | None:
        return self.db.query(ModelDisciplina).filter(ModelDisciplina.id == disciplina_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelDisciplina]:
        return self.db.query(ModelDisciplina).offset(skip).limit(limit).all()

    def update(self, disciplina_id: int, dados: DisciplinaUpdate) -> ModelDisciplina | None:
        disciplina = self.get_byID(disciplina_id)
        if not disciplina:
            return None

        if dados.nome is not None:
            disciplina.nome = dados.nome
        if dados.codigo is not None:
            disciplina.codigo = dados.codigo
        if dados.carga_horaria is not None:
            disciplina.carga_horaria = dados.carga_horaria
        if dados.turma_id is not None:
            disciplina.turma_id = dados.turma_id

        self.db.commit()
        self.db.refresh(disciplina)
        return disciplina

    def delete(self, disciplina_id: int) -> bool:
        disciplina = self.get_byID(disciplina_id)
        if not disciplina:
            return False
        self.db.delete(disciplina)
        self.db.commit()
        return True
