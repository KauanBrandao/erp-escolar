from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from models.ModelTurma import ModelTurma
from schemas.SchemaTurma import TurmaCreate, TurmaUpdate

class TurmaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: TurmaCreate) -> ModelTurma:
        db_obj = ModelTurma(data.model_dump(),criado_em = date.today())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def get_by_id(self, obj_id: int) -> Optional[ModelTurma]:
        return self.db.query(ModelTurma).filter(ModelTurma.id == obj_id).first()
    
    def get_byID(self, obj_id: int) -> Optional[ModelTurma]:
        return self.get_by_id(obj_id)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelTurma]:
        return self.db.query(ModelTurma).offset(skip).limit(limit).all()

    def update(self, obj_id: int, data: TurmaUpdate) -> Optional[ModelTurma]:
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
