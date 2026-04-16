from fastapi import HTTPException
from sqlalchemy.orm import Session

from repositories.RepositoryAluno import AlunoRepository
from schemas.SchemaAluno import AlunoCreate, AlunoUpdate


class ServiceAluno:
    def __init__(self, db: Session):
        self.repository = AlunoRepository(db)

    def criar(self, dados: AlunoCreate):
        return self.repository.create(dados)

    def buscar_por_id(self, aluno_id: int):
        aluno = self.repository.get_byID(aluno_id)
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        return aluno

    def listar(self):
        return self.repository.get_all()

    def atualizar(self, aluno_id: int, dados: AlunoUpdate):
        aluno = self.repository.update(aluno_id, dados)
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        return aluno

    def deletar(self, aluno_id: int):
        sucesso = self.repository.delete(aluno_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        return {"mensagem": "Aluno deletado com sucesso"}
