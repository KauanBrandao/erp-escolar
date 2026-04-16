from sqlalchemy.orm import Session

from repositories.RepositoryMensalidade import MensalidadeRepository


class ServiceMensalidade:
    def __init__(self, db: Session):
        self.repo = MensalidadeRepository(db)

    def create(self, data):
        return self.repo.create(data)

    def get_by_id(self, obj_id: int):
        return self.repo.get_byID(obj_id)

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip, limit)

    def update(self, obj_id: int, data):
        return self.repo.update(obj_id, data)

    def delete(self, obj_id: int):
        return self.repo.delete(obj_id)