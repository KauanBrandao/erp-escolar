from datetime import date

from database import Base
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String


class ModelMensalidade(Base):
    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer,ForeignKey("Alunos.id"), nullable=False)
    mes = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    valor = Column(Float, nullable=False)
    vencimento = Column(Date, nullable=False)
    status = Column(String(30), nullable=False, default="ativa")
