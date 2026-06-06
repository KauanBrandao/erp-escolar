from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.database import SessionLocal
from core.rbac import has_permission
from core.security import decodificar_token
from models.ModelPerfil import ModelPerfil
from models.ModelUsuario import ModelUsuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@dataclass
class AuthContext:
    usuario: ModelUsuario
    perfil: ModelPerfil


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> AuthContext:
    payload = decodificar_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido",
        )

    usuario = db.query(ModelUsuario).filter(ModelUsuario.id == int(user_id)).first()
    if not usuario or not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario nao autorizado",
        )

    perfil = db.query(ModelPerfil).filter(ModelPerfil.id == usuario.perfil_id).first()
    if not perfil:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Perfil do usuario nao encontrado",
        )

    return AuthContext(usuario=usuario, perfil=perfil)


def require_permission(permission: str):
    def permission_dependency(auth: AuthContext = Depends(get_current_user)) -> AuthContext:
        if not has_permission(auth.perfil.nome, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissao para este recurso",
            )
        return auth

    return permission_dependency
