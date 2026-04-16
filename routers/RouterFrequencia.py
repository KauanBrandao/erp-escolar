from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.database import SessionLocal
from schemas.SchemaFrequencia import (FrequenciaCreate, FrequenciaResponse,
                                      FrequenciaUpdate)
from services.ServiceFrequencia import ServiceFrequencia

router = APIRouter(prefix="/frequencias", tags=["Frequencias"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=FrequenciaResponse, status_code=201)
def criar_aluno(dados: FrequenciaCreate, db: Session = Depends(get_db)):
    return ServiceFrequencia(db).criar(dados)


@router.get("/", response_model=list[FrequenciaResponse])
def listar_alunos(db: Session = Depends(get_db)):
    return ServiceFrequencia(db).listar()


@router.get("/{frequencia_id}", response_model=FrequenciaResponse)
def buscar_aluno(frequencia_id: int, db: Session = Depends(get_db)):
    return ServiceFrequencia(db).buscar_por_id(frequencia_id)


@router.put("/{frequencia_id}", response_model=FrequenciaResponse)
def atualizar_aluno(frequencia_id: int, dados: FrequenciaUpdate, db: Session = Depends(get_db)):
    return ServiceFrequencia(db).atualizar(frequencia_id, dados)


@router.delete("/{frequencia_id}")
def deletar_aluno(frequencia_id: int, db: Session = Depends(get_db)):
    return ServiceFrequencia(db).deletar(frequencia_id)
