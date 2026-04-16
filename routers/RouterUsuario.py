from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.database import SessionLocal
from schemas.SchemaUsuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from services.ServiceUsuario import ServiceUsuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UsuarioResponse, status_code=201)
def criar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    return ServiceUsuario(db).criar(dados)


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuario(db: Session = Depends(get_db)):
    return ServiceUsuario(db).listar()


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def buscar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return ServiceUsuario(db).buscar_por_id(usuario_id)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: int, dados: UsuarioUpdate, db: Session = Depends(get_db)):
    return ServiceUsuario(db).atualizar(usuario_id, dados)


@router.delete("/{usuario_id}")
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return ServiceUsuario(db).deletar(usuario_id)
