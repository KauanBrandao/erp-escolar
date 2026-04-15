from models.database import Base
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String


class ModelPagamento(Base):
    __tablename__ = "Pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    data_pagamento = Column(Date, nullable=False)
    valor_pago = Column(Float, nullable=False)
    forma_pagamento = Column(String(50), nullable=False) 
    comprovante = Column(String(255), nullable=True)     
    mensalidade_id = Column(Integer, ForeignKey("Mensalidades.id"), nullable=False)    # Chave estrangeira ligando à tabela de Mensalidades