from models.database import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey

class ModelUsuario(Base):
    __tablename__ = "Usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    ativo = Column(Boolean, nullable=False)
    criado_em = Column(Date, nullable=False)
    perfil_id = Column(Integer, ForeignKey("Perfis.id"))
