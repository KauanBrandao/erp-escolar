from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.database import SessionLocal
from schemas.SchemaResponsavel import (ResponsavelCreate, ResponsavelResponse,
                                       ResponsavelUpdate)
from services.ServiceResponsavel import ServiceResponsavel

router = APIRouter(prefix="/responsaveis", tags=["Responsaveis"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ResponsavelResponse, status_code=201)
def criar_responsavel(dados: ResponsavelCreate, db: Session = Depends(get_db)):
    return ServiceResponsavel(db).criar(dados)


@router.get("/", response_model=list[ResponsavelResponse])
def listar_responsavel(db: Session = Depends(get_db)):
    return ServiceResponsavel(db).listar()


@router.get("/{responsavel_id}", response_model=ResponsavelResponse)
def buscar_responsavel(responsavel_id: int, db: Session = Depends(get_db)):
    return ServiceResponsavel(db).buscar_por_id(responsavel_id)


@router.put("/{responsavel_id}", response_model=ResponsavelResponse)
def atualizar_responsavel(responsavel_id: int, dados: ResponsavelUpdate, db: Session = Depends(get_db)):
    return ServiceResponsavel(db).atualizar(responsavel_id, dados)


@router.delete("/{responsavel_id}")
def deletar_responsavel(responsavel_id: int, db: Session = Depends(get_db)):
    return ServiceResponsavel(db).deletar(responsavel_id)

