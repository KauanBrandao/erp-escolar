from sqlalchemy.orm import Session

from models.ModelPagamento import ModelPagamento
from repositories.RepositoryMensalidade import MensalidadeRepository


class ServiceMensalidade:
    def __init__(self, db: Session):
        self.repo = MensalidadeRepository(db)

    def criar(self, data):
        return self.repo.create(data)

    def buscar_por_id(self, obj_id: int):
        return self.repo.get_byID(obj_id)

    def listar(self, skip: int = 0):
        return self.repo.get_all(skip)

    def atualizar(self, obj_id: int, data):
        return self.repo.update(obj_id, data)

    def deletar(self, obj_id: int):
        db = self.repo.db
        db.query(ModelPagamento).filter(
            ModelPagamento.mensalidade_id == obj_id
        ).delete(synchronize_session=False)
        db.commit()
        return self.repo.delete(obj_id)
