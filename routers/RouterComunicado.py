from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.database import SessionLocal
from schemas.SchemaComunicado import (ComunicadoCreate, ComunicadoResponse,
                                      ComunicadoUpdate)
from services.ServiceComunicado import ServiceComunicado

router = APIRouter(prefix="/comunicados", tags=["Alunos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ComunicadoResponse, status_code=201)
def criar_aluno(dados: ComunicadoCreate, db: Session = Depends(get_db)):
    return ServiceComunicado(db).criar(dados)


@router.get("/", response_model=list[ComunicadoResponse])
def listar_alunos(db: Session = Depends(get_db)):
    return ServiceComunicado(db).listar()


@router.get("/{comunicado_id}", response_model=ComunicadoResponse)
def buscar_aluno(comunicado_id: int, db: Session = Depends(get_db)):
    return ServiceComunicado(db).buscar_por_id(comunicado_id)


@router.put("/{comunicado_id}", response_model=ComunicadoResponse)
def atualizar_aluno(comunicado_id: int, dados: ComunicadoUpdate, db: Session = Depends(get_db)):
    return ServiceComunicado(db).atualizar(comunicado_id, dados)


@router.delete("/{comunicado_id}")
def deletar_aluno(comunicado_id: int, db: Session = Depends(get_db)):
    return ServiceComunicado(db).deletar(comunicado_id)
