from datetime import date

from sqlalchemy.orm import Session

from models.ModelAluno import ModelAluno
from schemas.SchemaAluno import AlunoCreate, AlunoUpdate


class AlunoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, aluno: AlunoCreate) -> ModelAluno:
        db_aluno = ModelAluno(**aluno.model_dump(), criado_em=date.today())
        self.db.add(db_aluno)
        self.db.commit()
        self.db.refresh(db_aluno)
        return db_aluno

    def get_byID(self, aluno_id: int) -> ModelAluno | None:
        return self.db.query(ModelAluno).filter(ModelAluno.id == aluno_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelAluno]:
        return self.db.query(ModelAluno).offset(skip).limit(limit).all()

    def update(self, aluno_id: int, dados: AlunoUpdate) -> ModelAluno | None:
        aluno = self.get_byID(aluno_id)
        if not aluno:
            return None

        if dados.nome is not None:
            aluno.nome = dados.nome
        if dados.telefone is not None:
            aluno.telefone = dados.telefone
        if dados.ativo is not None:
            aluno.ativo = dados.ativo

        self.db.commit()
        self.db.refresh(aluno)
        return aluno

    def delete(self, aluno_id: int) -> bool:
        aluno = self.get_byID(aluno_id)
        if not aluno:
            return False
        self.db.delete(aluno)
        self.db.commit()
        return True
