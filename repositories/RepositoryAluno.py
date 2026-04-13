from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session

from models.ModelAluno import ModelAluno
from schemas.SchemaAluno import AlunoCreate, AlunoUpdate


class AlunoRepository:
    def __init__(self, db:Session):
        self.db = db

    def create(self, aluno:AlunoCreate) -> ModelAluno:
        db_aluno = ModelAluno(**aluno.model_dump(),criado_em=date.today() ) # Transforma o Pydantic em dicionário & Define a data de criação manualmente
        self.db.add(db_aluno)
        self.db.commit()
        self.db.refresh(db_aluno)
        return db_aluno
    
    def get_byID(self,aluno_id:id) -> Optional[ModelAluno]:
        return self.db.query(ModelAluno).filter(ModelAluno.id == aluno_id).first()

    def get_all(self, skip:int = 0, limit: int = 100) -> List[ModelAluno]:
        return self.db.query(ModelAluno).offset(skip).limit(limit).all()
    
    def update(self, aluno_id: int, aluno_data: AlunoUpdate) -> Optional[ModelAluno]:
        db_aluno = self.db.get(aluno_id)
        if db_aluno:
            # .model_dump(exclude_unset=True) garante que só atualizaremos 
            # os campos que o usuário de fato enviou no JSON
            update_data = aluno_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_aluno, key, value) # seta os atributos dinamicamente
        
            self.db.commit()
            self.db.refresh(db_aluno)
        return db_aluno
    
    def delete(self, aluno_id:int) -> bool:
        db_aluno = self.get(aluno_id)
        if db_aluno:
            self.db.delete(db_aluno)
            self.db.commit()
            return True
        return False