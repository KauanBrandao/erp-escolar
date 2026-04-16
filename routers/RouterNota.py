from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.database import SessionLocal
from services.ServiceNota import ServiceNota
from schemas.SchemaNota import NotaCreate, NotaResponse, NotaUpdate

router = APIRouter(prefix="/notas", tags=["Notas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=NotaResponse, status_code=201)
def criar_nota(dados: NotaCreate, db: Session = Depends(get_db)):
    return ServiceNota(db).criar(dados)


@router.get("/", response_model=list[NotaResponse])
def listar_notas(db: Session = Depends(get_db)):
    return ServiceNota(db).listar()


@router.get("/{nota_id}", response_model=NotaResponse)
def buscar_nota(nota_id: int, db: Session = Depends(get_db)):
    return ServiceNota(db).buscar_por_id(nota_id)


@router.put("/{nota_id}", response_model=NotaResponse)
def atualizar_nota(nota_id: int, dados: NotaUpdate, db: Session = Depends(get_db)):
    return ServiceNota(db).atualizar(nota_id, dados)


@router.delete("/{nota_id}")
def deletar_nota(nota_id: int, db: Session = Depends(get_db)):
    return ServiceNota(db).deletar(nota_id)
