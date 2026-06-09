from fastapi import HTTPException
from sqlalchemy.orm import Session
from repositories.RepositoryUsuario import UsuarioRepository


class ServiceUsuario:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def criar(self, data):
        if self.repo.get_by_email(data.email):
            raise HTTPException(status_code=409, detail="E-mail já cadastrado no sistema")
        return self.repo.create(data)

    def buscar_por_id(self, obj_id: int):
        obj = self.repo.get_byID(obj_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return obj

    def listar(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip, limit)

    def atualizar(self, obj_id: int, data):
        obj = self.repo.update(obj_id, data)
        if not obj:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return obj

    def deletar(self, obj_id: int):
        sucesso = self.repo.delete(obj_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return {"mensagem": "Usuário deletado com sucesso"}
