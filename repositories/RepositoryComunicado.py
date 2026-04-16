from sqlalchemy.orm import Session

from models.ModelComunicado import ModelComunicado
from schemas.SchemaComunicado import ComunicadoCreate, ComunicadoUpdate


class ComunicadoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, comunicado: ComunicadoCreate) -> ModelComunicado:
        db_comunicado = ModelComunicado(**comunicado.model_dump())
        self.db.add(db_comunicado)
        self.db.commit()
        self.db.refresh(db_comunicado)
        return db_comunicado

    def get_byID(self, comunicado_id: int) -> ModelComunicado | None:
        return self.db.query(ModelComunicado).filter(ModelComunicado.id == comunicado_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelComunicado]:
        return self.db.query(ModelComunicado).offset(skip).limit(limit).all()

    def update(self, comunicado_id: int, dados: ComunicadoUpdate) -> ModelComunicado | None:
        comunicado = self.get_byID(comunicado_id)
        if not comunicado:
            return None

        if dados.titulo is not None:
            comunicado.titulo = dados.titulo
        if dados.conteudo is not None:
            comunicado.conteudo = dados.conteudo
        if dados.ativo is not None:
            comunicado.ativo = dados.ativo

        self.db.commit()
        self.db.refresh(comunicado)
        return comunicado

    def delete(self, comunicado_id: int) -> bool:
        comunicado = self.get_byID(comunicado_id)
        if not comunicado:
            return False
        self.db.delete(comunicado)
        self.db.commit()
        return True
