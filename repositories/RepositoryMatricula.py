from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from models.ModelMatricula import ModelMatricula
from schemas.SchemaMatricula import MatriculaCreate, MatriculaUpdate


class MatriculaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: MatriculaCreate) -> ModelMatricula:
        db_obj = ModelMatricula(**data.model_dump(), criado_em=date.today())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get_by_id(self, obj_id: int) -> Optional[ModelMatricula]:
        return self.db.query(ModelMatricula).filter(ModelMatricula.id == obj_id).first()

    def get_byID(self, obj_id: int) -> Optional[ModelMatricula]:
        return self.get_by_id(obj_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelMatricula]:
        return self.db.query(ModelMatricula).offset(skip).limit(limit).all()

    def update(self, obj_id: int, data: MatriculaUpdate) -> Optional[ModelMatricula]:
        db_obj = self.get_by_id(obj_id)
        if not db_obj:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_obj, key, value)

        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, obj_id: int) -> bool:
        db_obj = self.get_by_id(obj_id)
        if not db_obj:
            return False

        self.db.delete(db_obj)
        self.db.commit()
        return True
