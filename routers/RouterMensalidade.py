from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.database import SessionLocal
from schemas.SchemaMensalidade import (MensalidadeCreate, MensalidadeResponse,
                                       MensalidadeUpdate)
from services.ServiceMensalidade import ServiceMensalidade

router = APIRouter(prefix="/mensalidades", tags=["Mensalidade"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=MensalidadeResponse, status_code=201)
def criar_mensalidade(dados: MensalidadeCreate, db: Session = Depends(get_db)):
    return ServiceMensalidade(db).criar(dados)


@router.get("/", response_model=list[MensalidadeResponse])
def listar_mensalidade(db: Session = Depends(get_db)):
    return ServiceMensalidade(db).listar()


@router.get("/{mensalidade_id}", response_model=MensalidadeResponse)
def buscar_mensalidade(mensalidade_id: int, db: Session = Depends(get_db)):
    return ServiceMensalidade(db).buscar_por_id(mensalidade_id)


@router.put("/{mensalidade_id}", response_model=MensalidadeResponse)
def atualizar_mensalidade(mensalidade_id: int, dados: MensalidadeUpdate, db: Session = Depends(get_db)):
    return ServiceMensalidade(db).atualizar(mensalidade_id, dados)


@router.delete("/{mensalidade_id}")
def deletar_mensalidade(mensalidade_id: int, db: Session = Depends(get_db)):
    return ServiceMensalidade(db).deletar(mensalidade_id)
