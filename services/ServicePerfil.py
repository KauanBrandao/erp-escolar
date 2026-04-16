from sqlalchemy.orm import Session

from repositories.RepositoryPerfil import PerfilRepository


class ServicePerfil:
    def __init__(self, db: Session):
        self.repo = PerfilRepository(db)

    def criar(self, data):
        return self.repo.create(data)

    def buscar_por_id(self, obj_id: int):
        return self.repo.get_byID(obj_id)

    def listar(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip, limit)

    def atualizar(self, obj_id: int, data):
        return self.repo.update(obj_id, data)

    def deletar(self, obj_id: int):
        return self.repo.delete(obj_id)