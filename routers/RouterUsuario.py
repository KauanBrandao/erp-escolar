from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from domain.UsuarioDominio import criar_usuario_dominio
from models.ModelPerfil import ModelPerfil
from models.database import SessionLocal
from schemas.SchemaUsuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from services.ServiceUsuario import ServiceUsuario
from utils.logger import registrar_log

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UsuarioResponse, status_code=201)
def criar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    usuario = ServiceUsuario(db).criar(dados)
    registrar_log(dados.email, f"Cadastro de usuario: {dados.nome}")
    return usuario


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuario(db: Session = Depends(get_db)):
    
    return ServiceUsuario(db).listar()


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def buscar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return ServiceUsuario(db).buscar_por_id(usuario_id)


@router.get("/{usuario_id}/permissoes")
def ver_permissoes(usuario_id: int, db: Session = Depends(get_db)):
    """Retorna as permissões do usuário conforme seu perfil (polimorfismo em ação)."""
    usuario = ServiceUsuario(db).buscar_por_id(usuario_id)
    perfil = db.query(ModelPerfil).filter(ModelPerfil.id == usuario.perfil_id).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")

    dominio = criar_usuario_dominio(usuario.nome, usuario.email, perfil.nome)
    return {
        "usuario": str(dominio),
        "perfil": perfil.nome,
        "permissoes": dominio.get_permissoes(),
        "pode_deletar": dominio.pode_deletar(),
    }


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: int, dados: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = ServiceUsuario(db).atualizar(usuario_id, dados)
    registrar_log("sistema", f"Atualizacao de usuario ID {usuario_id}")
    return usuario


@router.delete("/{usuario_id}")
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    resultado = ServiceUsuario(db).deletar(usuario_id)
    registrar_log("sistema", f"Remocao de usuario ID {usuario_id}")
    return resultado
