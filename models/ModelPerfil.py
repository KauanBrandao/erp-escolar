from .database import Base
from sqlalchemy import Column, Integer, String

class ModelPerfil(Base):
    __tablename__ = "Perfil"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String) 