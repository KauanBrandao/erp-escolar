from fastapi import HTTPException
from sqlalchemy.orm import Session

from repositories.RepositoryTurma import TurmaRepository
from schemas.SchemaTurma import TurmaCreate, TurmaUpdate


class ServiceTurma:
    def __init__(self, db: Session):
        self.repository = TurmaRepository(db)

    def criar(self, dados: TurmaCreate):
        return self.repository.create(dados)

    def buscar_por_id(self, turma_id: int):
        turma = self.repository.get_byID(turma_id)
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        return turma

    def listar(self):
        return self.repository.get_all()

    def atualizar(self, turma_id: int, dados: TurmaUpdate):
        turma = self.repository.update(turma_id, dados)
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        return turma

    def deletar(self, turma_id: int):
        sucesso = self.repository.delete(turma_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        return {"mensagem": "Turma deletada com sucesso"}
