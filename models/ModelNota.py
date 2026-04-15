from models.database import Base
from sqlalchemy import Column, Integer, Numeric, String, Date, ForeignKey

class ModelNota(Base):
    __tablename__= "Notas"

    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Numeric(4, 2), nullable=False)       
    tipo = Column(String(30), nullable=False)         # prova, trabalho, recuperacao
    bimestre = Column(Integer, nullable=False)          
    lancado_em = Column(Date, nullable=False)
    aluno_id = Column(Integer, ForeignKey("Alunos.id"), nullable=False)
    disciplina_id = Column(Integer, ForeignKey("Disciplinas.id"), nullable=False)

    
