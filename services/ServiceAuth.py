from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.security import criar_access_token, verificar_senha
from repositories.RepositoryPerfil import PerfilRepository
from repositories.RepositoryUsuario import UsuarioRepository


class ServiceAuth:
    def __init__(self, db: Session):
        self.usuario_repository = UsuarioRepository(db)
        self.perfil_repository = PerfilRepository(db)

    def login(self, email: str, senha: str):
        usuario = self.usuario_repository.get_by_email(email)
        if not usuario or not verificar_senha(senha, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha invalidos",
            )

        if not usuario.ativo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inativo",
            )

        perfil = self.perfil_repository.get_byID(usuario.perfil_id)
        if not perfil:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Perfil do usuario nao encontrado",
            )

        access_token = criar_access_token(
            {
                "sub": str(usuario.id),
                "perfil_id": perfil.id,
                "perfil_nome": perfil.nome,
                "type": "access",
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
