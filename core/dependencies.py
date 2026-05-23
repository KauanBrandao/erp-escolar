from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from core.security import SECRET_KEY, ALGORITHM
from models.database import SessionLocal
from models.ModelUsuario import ModelUsuario
from models.ModelPerfil import ModelPerfil

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(ModelUsuario).filter(ModelUsuario.email == email).first()
    if user is None:
        raise credentials_exception
    if not user.ativo:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return user

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = [role.lower() for role in allowed_roles]

    def __call__(self, current_user: ModelUsuario = Depends(get_current_user), db: Session = Depends(get_db)):
        perfil = db.query(ModelPerfil).filter(ModelPerfil.id == current_user.perfil_id).first()
        if not perfil or perfil.nome.lower() not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="O usuário não tem privilégios suficientes"
            )
        return current_user

# Perfis definidos: administrador, secretaria, coordenação pedagógica, financeiro, responsavel
require_admin = RoleChecker(["administrador"])
require_secretaria = RoleChecker(["administrador", "secretaria"])
require_coordenacao = RoleChecker(["administrador", "coordenação pedagógica", "coordenação pedagogica"])
require_financeiro = RoleChecker(["administrador", "financeiro"])
require_responsavel = RoleChecker(["administrador", "responsavel", "responsável"])

