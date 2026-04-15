from sqlalchemy.orm import Session
from repositories.RepositoryAluno import AlunoRepository
from schemas.SchemaAluno import AlunoCreate, AlunoUpdate

class ServiceAluno:
    def __init__(self, db: Session):
        self.repo = AlunoRepository(db)

    def create(self, aluno: AlunoCreate):
        return self.repo.create(aluno)

    def get_by_id(self, aluno_id: int):
        return self.repo.get_byID(aluno_id)

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip, limit)

    def update(self, aluno_id: int, aluno_data: AlunoUpdate):
        return self.repo.update(aluno_id, aluno_data)

    def delete(self, aluno_id: int):
        return self.repo.delete(aluno_id)