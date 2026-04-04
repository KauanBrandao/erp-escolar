from database import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey

class ModelUsuario(Base):
    __tablename__ = "Usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String, nullable=False)
    senha_hash = Column(String, nullable=False)
    ativo = Column(Boolean, nullable=False)
    criado_em = Column(Date, nullable=False)
    perfil_id = Column(Integer, ForeignKey("Perfis.id"))
