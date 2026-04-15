from models.database import Base
from sqlalchemy import Column, Integer, String

class ModelPerfil(Base):
    __tablename__ = "Perfis"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(250)) 