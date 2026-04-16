from sqlalchemy.orm import Session

from models.ModelPerfil import ModelPerfil
from schemas.SchemaPerfil import PerfilCreate, PerfilUpdate


class PerfilRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, perfil: PerfilCreate) -> ModelPerfil:
        db_perfil = ModelPerfil(**perfil.model_dump())
        self.db.add(db_perfil)
        self.db.commit()
        self.db.refresh(db_perfil)
        return db_perfil

    def get_byID(self, perfil_id: int) -> ModelPerfil | None:
        return self.db.query(ModelPerfil).filter(ModelPerfil.id == perfil_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelPerfil]:
        return self.db.query(ModelPerfil).offset(skip).limit(limit).all()

    def update(self, perfil_id: int, dados: PerfilUpdate) -> ModelPerfil | None:
        perfil = self.get_byID(perfil_id)
        if not perfil:
            return None

        if dados.nome is not None:
            perfil.nome = dados.nome
        if dados.descricao is not None:
            perfil.descricao = dados.descricao

        self.db.commit()
        self.db.refresh(perfil)
        return perfil

    def delete(self, perfil_id: int) -> bool:
        perfil = self.get_byID(perfil_id)
        if not perfil:
            return False
        self.db.delete(perfil)
        self.db.commit()
        return True
