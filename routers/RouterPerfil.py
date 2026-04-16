from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.database import SessionLocal
from schemas.SchemaPerfil import PerfilCreate, PerfilResponse, PerfilUpdate
from services.ServicePerfil import ServicePerfil

router = APIRouter(prefix="/perfis", tags=["Perfil"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PerfilResponse, status_code=201)
def criar_aluno(dados: PerfilCreate, db: Session = Depends(get_db)):
    return ServicePerfil(db).criar(dados)


@router.get("/", response_model=list[PerfilResponse])
def listar_alunos(db: Session = Depends(get_db)):
    return ServicePerfil(db).listar()


@router.get("/{perfil_id}", response_model=PerfilResponse)
def buscar_aluno(perfil_id: int, db: Session = Depends(get_db)):
    return ServicePerfil(db).buscar_por_id(perfil_id)


@router.put("/{perfil_id}", response_model=PerfilResponse)
def atualizar_aluno(perfil_id: int, dados: PerfilUpdate, db: Session = Depends(get_db)):
    return ServicePerfil(db).atualizar(perfil_id, dados)


@router.delete("/{perfil_id}")
def deletar_aluno(perfil_id: int, db: Session = Depends(get_db)):
    return ServicePerfil(db).deletar(perfil_id)
