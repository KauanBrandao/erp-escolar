from fastapi import HTTPException
from sqlalchemy.orm import Session

from repositories.RepositoryNota import NotaRepository
from repositories.RepositoryAluno import AlunoRepository
from schemas.SchemaNota import NotaCreate, NotaUpdate


class ServiceNota:
    def __init__(self, db: Session):
        self.repository = NotaRepository(db)
        self.aluno_repo = AlunoRepository(db)

    def criar(self, dados: NotaCreate):
        if not self.aluno_repo.get_byID(dados.aluno_id):
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        return self.repository.create(dados)

    def buscar_por_id(self, nota_id: int):
        nota = self.repository.get_byID(nota_id)
        if not nota:
            raise HTTPException(status_code=404, detail="Nota não encontrada")
        return nota

    def listar(self):
        return self.repository.get_all()

    def atualizar(self, nota_id: int, dados: NotaUpdate):
        nota = self.repository.update(nota_id, dados)
        if not nota:
            raise HTTPException(status_code=404, detail="Nota não encontrada")
        return nota

    def deletar(self, nota_id: int):
        sucesso = self.repository.delete(nota_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Nota não encontrada")
        return {"mensagem": "Nota deletada com sucesso"}
