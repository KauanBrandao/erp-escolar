from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.database import SessionLocal
from schemas.SchemaDisciplina import (DisciplinaCreate, DisciplinaResponse,
                                      DisciplinaUpdate)
from services.ServiceDisciplina import ServiceDisciplina

router = APIRouter(prefix="/disciplinas", tags=["Disciplinas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=DisciplinaResponse, status_code=201)
def criar_aluno(dados: DisciplinaCreate, db: Session = Depends(get_db)):
    return ServiceDisciplina(db).criar(dados)


@router.get("/", response_model=list[DisciplinaResponse])
def listar_alunos(db: Session = Depends(get_db)):
    return ServiceDisciplina(db).listar()


@router.get("/{disciplina_id}", response_model=DisciplinaResponse)
def buscar_aluno(disciplina_id: int, db: Session = Depends(get_db)):
    return ServiceDisciplina(db).buscar_por_id(disciplina_id)


@router.put("/{disciplina_id}", response_model=DisciplinaResponse)
def atualizar_aluno(disciplina_id: int, dados: DisciplinaUpdate, db: Session = Depends(get_db)):
    return ServiceDisciplina(db).atualizar(disciplina_id, dados)


@router.delete("/{disciplina_id}")
def deletar_aluno(disciplina_id: int, db: Session = Depends(get_db)):
    return ServiceDisciplina(db).deletar(disciplina_id)
