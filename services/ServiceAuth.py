from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.rbac import normalize_profile_name
from core.security import criar_access_token, verificar_senha
from models.ModelUsuario import ModelUsuario
from repositories.RepositoryPerfil import PerfilRepository
from repositories.RepositoryUsuario import UsuarioRepository
from schemas.SchemaPerfil import PerfilCreate
from schemas.SchemaUsuario import UsuarioCreate


class ServiceAuth:
    def __init__(self, db: Session):
        self.db = db
        self.usuario_repository = UsuarioRepository(db)
        self.perfil_repository = PerfilRepository(db)

    def setup_admin(self, nome: str, email: str, senha: str):
        if self._admin_ja_existe():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Setup bloqueado: ja existe usuario administrador",
            )

        if self.usuario_repository.get_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ja existe usuario com este email",
            )

        perfil_admin = self._obter_ou_criar_perfil_admin()
        usuario = UsuarioCreate(
            nome=nome,
            email=email,
            senha=senha,
            ativo=True,
            perfil_id=perfil_admin.id,
        )
        return self.usuario_repository.create(usuario)

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

    def _obter_ou_criar_perfil_admin(self):
        perfis = self.perfil_repository.get_all(skip=0, limit=1000)
        for perfil in perfis:
            if normalize_profile_name(perfil.nome) == "administrador":
                return perfil

        return self.perfil_repository.create(
            PerfilCreate(
                nome="Administrador",
                descricao="Gestao global do sistema",
            )
        )

    def _admin_ja_existe(self) -> bool:
        perfis = self.perfil_repository.get_all(skip=0, limit=1000)
        admin_profile_ids = [
            perfil.id for perfil in perfis if normalize_profile_name(perfil.nome) == "administrador"
        ]
        if not admin_profile_ids:
            return False

        return (
            self.db.query(ModelUsuario)
            .filter(ModelUsuario.perfil_id.in_(admin_profile_ids))
            .first()
            is not None
        )
