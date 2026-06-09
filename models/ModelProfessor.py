from datetime import date

from core.database import Base
from sqlalchemy import Boolean, Column, Date, Integer, String


class ModelProfessor(Base):
    __tablename__ = "Professores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(15), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    telefone = Column(String(20), nullable=False)
    especialidade = Column(String(100), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(Date, nullable=False)
