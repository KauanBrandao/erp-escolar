import hashlib
from datetime import date

from sqlalchemy.orm import Session

from models.ModelUsuario import ModelUsuario
from schemas.SchemaUsuario import UsuarioCreate, UsuarioUpdate


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, usuario: UsuarioCreate) -> ModelUsuario:
        dados = usuario.model_dump()
        senha_hash = hashlib.sha256(dados.pop("senha").encode()).hexdigest()
        db_usuario = ModelUsuario(**dados, senha_hash=senha_hash, criado_em=date.today())
        self.db.add(db_usuario)
        self.db.commit()
        self.db.refresh(db_usuario)
        return db_usuario

    def get_byID(self, usuario_id: int) -> ModelUsuario | None:
        return self.db.query(ModelUsuario).filter(ModelUsuario.id == usuario_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelUsuario]:
        return self.db.query(ModelUsuario).offset(skip).limit(limit).all()

    def update(self, usuario_id: int, dados: UsuarioUpdate) -> ModelUsuario | None:
        usuario = self.get_byID(usuario_id)
        if not usuario:
            return None

        if dados.nome is not None:
            usuario.nome = dados.nome
        if dados.email is not None:
            usuario.email = dados.email
        if dados.ativo is not None:
            usuario.ativo = dados.ativo
        if dados.perfil_id is not None:
            usuario.perfil_id = dados.perfil_id

        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def delete(self, usuario_id: int) -> bool:
        usuario = self.get_byID(usuario_id)
        if not usuario:
            return False
        self.db.delete(usuario)
        self.db.commit()
        return True
