from models.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger

class ModelResponsavel(Base):
    __tablename__ = "Responsaveis"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(15), nullable=False, unique=True)
    telefone = Column(BigInteger, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    parentesco = Column(Integer, ForeignKey("Usuarios.id"))
