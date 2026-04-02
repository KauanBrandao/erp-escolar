from database import Base
from sqlalchemy import (BigInteger, Boolean, Column, Date, ForeignKey, Integer,
                        String)


class ModelAluno(Base):
    __tablename__ = "Alunos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(15), nullable=False, unique=True)
    telefone = Column(BigInteger, nullable=False, unique=True)
    matricula_numero = Column(Integer, nullable=False, unique=True)
    ativo = Column(Boolean, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    criado_em = Column(Date, nullable=False)
    responsavel_id = Column(Integer, ForeignKey("Responsaveis.id"))

    responsavel_id = Column(Integer, ForeignKey("Responsaveis.id"))

