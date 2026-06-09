from fastapi import HTTPException
from sqlalchemy.orm import Session

from repositories.RepositoryProfessor import ProfessorRepository


class ServiceProfessor:
    def __init__(self, db: Session):
        self.repo = ProfessorRepository(db)

    def criar(self, data):
        if self.repo.get_by_cpf(data.cpf):
            raise HTTPException(status_code=409, detail="CPF já cadastrado no sistema")
        if self.repo.get_by_email(data.email):
            raise HTTPException(status_code=409, detail="E-mail já cadastrado no sistema")
        return self.repo.create(data)

    def buscar_por_id(self, obj_id: int):
        obj = self.repo.get_byID(obj_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Professor não encontrado")
        return obj

    def listar(self):
        return self.repo.get_all()

    def atualizar(self, obj_id: int, data):
        obj = self.repo.update(obj_id, data)
        if not obj:
            raise HTTPException(status_code=404, detail="Professor não encontrado")
        return obj

    def deletar(self, obj_id: int):
        if not self.repo.get_byID(obj_id):
            raise HTTPException(status_code=404, detail="Professor não encontrado")
        self.repo.delete(obj_id)
        return {"mensagem": "Professor deletado com sucesso"}
