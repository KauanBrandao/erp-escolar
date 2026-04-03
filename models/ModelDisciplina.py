from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class ModelDisciplina(Base):
    __tablename__ = "Disciplinas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    codigo = Column(String(20), nullable=False, unique=True)
    carga_horaria = Column(Integer, nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    
