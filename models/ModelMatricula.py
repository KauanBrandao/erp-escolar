from models.database import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey

class ModelMatricula(Base):
    __tablename__ = "Matriculas"

    id = Column(Integer,primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("Alunos.id"), nullable=False)
    turma_id = Column(Integer, ForeignKey("Turmas.id"), nullable=False)
    data_matricula = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default="ativa") #ou trancada, cancelada
    observacao = Column(String(250), nullable=True)

   
