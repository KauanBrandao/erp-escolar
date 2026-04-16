from fastapi import HTTPException
from sqlalchemy.orm import Session

from repositories.RepositoryMatricula import MatriculaRepository
from repositories.RepositoryAluno import AlunoRepository
from repositories.RepositoryTurma import TurmaRepository
from schemas.SchemaMatricula import MatriculaCreate, MatriculaUpdate


class ServiceMatricula:
    def __init__(self, db: Session):
        self.repository = MatriculaRepository(db)
        self.aluno_repo = AlunoRepository(db)
        self.turma_repo = TurmaRepository(db)

    def criar(self, dados: MatriculaCreate):
        if not self.aluno_repo.get_byID(dados.aluno_id):
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        if not self.turma_repo.get_byID(dados.turma_id):
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        return self.repository.create(dados)

    def buscar_por_id(self, matricula_id: int):
        matricula = self.repository.get_byID(matricula_id)
        if not matricula:
            raise HTTPException(status_code=404, detail="Matrícula não encontrada")
        return matricula

    def listar(self):
        return self.repository.get_all()

    def atualizar(self, matricula_id: int, dados: MatriculaUpdate):
        matricula = self.repository.update(matricula_id, dados)
        if not matricula:
            raise HTTPException(status_code=404, detail="Matrícula não encontrada")
        return matricula

    def deletar(self, matricula_id: int):
        sucesso = self.repository.delete(matricula_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Matrícula não encontrada")
        return {"mensagem": "Matrícula deletada com sucesso"}
