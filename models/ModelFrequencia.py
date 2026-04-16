from database import Base
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, Text


class ModelFrequencia(Base):
    __tablename__ = "Frequencias"

    id = Column(Integer, primary_key=True, index=True)
    data_aula = Column(Date, nullable=False)
    presente = Column(Boolean, nullable=False)
    justificativa = Column(Text, nullable=True)
    disciplina_id = Column(Integer, ForeignKey("Disciplinas.id"), nullable=False)
    aluno_id = Column(Integer, ForeignKey("Alunos.id"), nullable=False)