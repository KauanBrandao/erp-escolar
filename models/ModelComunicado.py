from datetime import date

from database import Base
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class ModelComunicado(Base):
    __tablename__ = "Comunicados"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    conteudo = Column(Text, nullable=False)
    destinatario_id = Column(Integer, ForeignKey("Usuarios.id"), nullable=False)
    enviado_em = Column(Date, default=date.today, nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    destinatario = relationship("ModelUsuario")