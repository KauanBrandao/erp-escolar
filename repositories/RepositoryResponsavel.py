from sqlalchemy.orm import Session

from models.ModelResponsavel import ModelResponsavel
from schemas.SchemaResponsavel import ResponsavelCreate, ResponsavelUpdate


class ResponsavelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, responsavel: ResponsavelCreate) -> ModelResponsavel:
        db_responsavel = ModelResponsavel(**responsavel.model_dump())
        self.db.add(db_responsavel)
        self.db.commit()
        self.db.refresh(db_responsavel)
        return db_responsavel

    def get_byID(self, responsavel_id: int) -> ModelResponsavel | None:
        return self.db.query(ModelResponsavel).filter(ModelResponsavel.id == responsavel_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelResponsavel]:
        return self.db.query(ModelResponsavel).offset(skip).limit(limit).all()

    def update(self, responsavel_id: int, dados: ResponsavelUpdate) -> ModelResponsavel | None:
        responsavel = self.get_byID(responsavel_id)
        if not responsavel:
            return None

        if dados.nome is not None:
            responsavel.nome = dados.nome
        if dados.email is not None:
            responsavel.email = dados.email
        if dados.parentesco is not None:
            responsavel.parentesco = dados.parentesco

        self.db.commit()
        self.db.refresh(responsavel)
        return responsavel

    def delete(self, responsavel_id: int) -> bool:
        responsavel = self.get_byID(responsavel_id)
        if not responsavel:
            return False
        self.db.delete(responsavel)
        self.db.commit()
        return True
