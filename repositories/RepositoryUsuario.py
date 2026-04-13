from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session

from models.ModelUsuario import ModelUsuario
from schemas.SchemaUsuario import UsuarioCreate, UsuarioUpdate


class UsuarioRepository:
    def __int__(self, db:Session):
        self.db = db
    
    def create(self, usuario:UsuarioCreate) -> ModelUsuario:
        db_usuario = ModelUsuario(**usuario.model_dump(), criado_em=date.today)
        self.db.add(db_usuario)
        self.db.commit()
        self.db.refresh(db_usuario)
        return db_usuario

    def get_byID(self, usuario_id:int) -> Optional[ModelUsuario]:
        return self.db.query(ModelUsuario).filter(ModelUsuario.id == usuario_id).first()
    
    def get_all(self, skip:int = 0, limit: int = 100) -> List[ModelUsuario]:
        return self.db.query(ModelUsuario).offset(skip).limit(limit).all()
    
    def update(self,usuario_id:int, usuario_data:UsuarioUpdate) -> Optional[ModelUsuario]:
        db_usuario = self.db.get(usuario_id)
        if db_usuario:
            update_data = usuario_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_usuario, key, value)
                self.db.commit()
                self.db.refresh(db_usuario)
        return db_usuario

    def delete(self, usuario_id:int) -> bool:
        db_usuario = self.db.get(usuario_id)
        if db_usuario:
            self.db.delete(db_usuario)
            self.db.commit()
            return True
        return False