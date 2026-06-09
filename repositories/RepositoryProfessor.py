from datetime import date

from sqlalchemy.orm import Session

from models.ModelProfessor import ModelProfessor
from schemas.SchemaProfessor import ProfessorCreate, ProfessorUpdate


class ProfessorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, professor: ProfessorCreate) -> ModelProfessor:
        db_professor = ModelProfessor(**professor.model_dump(), criado_em=date.today())
        self.db.add(db_professor)
        self.db.commit()
        self.db.refresh(db_professor)
        return db_professor

    def get_byID(self, professor_id: int) -> ModelProfessor | None:
        return self.db.query(ModelProfessor).filter(ModelProfessor.id == professor_id).first()

    def get_by_cpf(self, cpf: str) -> ModelProfessor | None:
        return self.db.query(ModelProfessor).filter(ModelProfessor.cpf == cpf).first()

    def get_by_email(self, email: str) -> ModelProfessor | None:
        return self.db.query(ModelProfessor).filter(ModelProfessor.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 5000) -> list[ModelProfessor]:
        return self.db.query(ModelProfessor).offset(skip).limit(limit).all()

    def update(self, professor_id: int, dados: ProfessorUpdate) -> ModelProfessor | None:
        professor = self.get_byID(professor_id)
        if not professor:
            return None
        if dados.nome is not None:
            professor.nome = dados.nome
        if dados.email is not None:
            professor.email = dados.email
        if dados.telefone is not None:
            professor.telefone = dados.telefone
        if dados.especialidade is not None:
            professor.especialidade = dados.especialidade
        if dados.ativo is not None:
            professor.ativo = dados.ativo
        self.db.commit()
        self.db.refresh(professor)
        return professor

    def delete(self, professor_id: int) -> bool:
        professor = self.get_byID(professor_id)
        if not professor:
            return False
        self.db.delete(professor)
        self.db.commit()
        return True
