from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.database import SessionLocal
from services.ServiceTurma import ServiceTurma
from schemas.SchemaTurma import TurmaCreate, TurmaResponse, TurmaUpdate

router = APIRouter(prefix="/turmas", tags=["Turmas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=TurmaResponse, status_code=201)
def criar_turma(dados: TurmaCreate, db: Session = Depends(get_db)):
    return ServiceTurma(db).criar(dados)


@router.get("/", response_model=list[TurmaResponse])
def listar_turmas(db: Session = Depends(get_db)):
    return ServiceTurma(db).listar()


@router.get("/{turma_id}", response_model=TurmaResponse)
def buscar_turma(turma_id: int, db: Session = Depends(get_db)):
    return ServiceTurma(db).buscar_por_id(turma_id)


@router.put("/{turma_id}", response_model=TurmaResponse)
def atualizar_turma(turma_id: int, dados: TurmaUpdate, db: Session = Depends(get_db)):
    return ServiceTurma(db).atualizar(turma_id, dados)


@router.delete("/{turma_id}")
def deletar_turma(turma_id: int, db: Session = Depends(get_db)):
    return ServiceTurma(db).deletar(turma_id)
