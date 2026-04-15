from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from models.ModelFrequencia import ModelFrequencia
from schemas.SchemaFrequencia import FrequenciaCreate, FrequenciaUpdate


class FrequenciaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: FrequenciaCreate) -> ModelFrequencia:
        db_obj = ModelFrequencia(**data.model_dump(), criado_em=date.today())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get_by_id(self, obj_id: int) -> Optional[ModelFrequencia]:
        return self.db.query(ModelFrequencia).filter(ModelFrequencia.id == obj_id).first()

    def get_byID(self, obj_id: int) -> Optional[ModelFrequencia]:
        return self.get_by_id(obj_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelFrequencia]:
        return self.db.query(ModelFrequencia).offset(skip).limit(limit).all()

    def update(self, obj_id: int, data: FrequenciaUpdate) -> Optional[ModelFrequencia]:
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