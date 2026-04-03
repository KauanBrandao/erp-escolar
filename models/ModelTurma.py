from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class ModelTurma(Base):
    __tablename__ = "Turmas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    serie = Column(String(50), nullable=False)
    turno = Column(String(20), nullable=False)
    ano_letivo = Column(Integer, nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    perfil_id = Column(Integer, ForeignKey("Usuarios.id"), nullable=True)

   
