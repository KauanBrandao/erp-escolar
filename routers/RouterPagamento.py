from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.database import SessionLocal
from schemas.SchemaPagamento import (PagamentoCreate, PagamentoResponse,
                                     PagamentoUpdate)
from services.ServicePagamento import ServicePagamento

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PagamentoResponse, status_code=201)
def criar_pagamento(dados: PagamentoCreate, db: Session = Depends(get_db)):
    return ServicePagamento(db).criar(dados)


@router.get("/", response_model=list[PagamentoResponse])
def listar_pagamento(db: Session = Depends(get_db)):
    return ServicePagamento(db).listar()


@router.get("/{pagamento_id}", response_model=PagamentoResponse)
def buscar_pagamento(pagamento_id: int, db: Session = Depends(get_db)):
    return ServicePagamento(db).buscar_por_id(pagamento_id)


@router.put("/{pagamento_id}", response_model=PagamentoResponse)
def atualizar_pagamento(pagamento_id: int, dados: PagamentoUpdate, db: Session = Depends(get_db)):
    return ServicePagamento(db).atualizar(pagamento_id, dados)


@router.delete("/{pagamento_id}")
def deletar_pagamento(pagamento_id: int, db: Session = Depends(get_db)):
    return ServicePagamento(db).deletar(pagamento_id)
