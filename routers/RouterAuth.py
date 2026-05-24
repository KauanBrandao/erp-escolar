from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.auth_dependencies import AuthContext, get_current_user
from core.database import SessionLocal
from schemas.SchemaAuth import LoginRequest, MeResponse, TokenResponse
from services.ServiceAuth import ServiceAuth

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return ServiceAuth(db).login(payload.email, payload.senha)


@router.post("/token", response_model=TokenResponse)
def token(payload: LoginRequest, db: Session = Depends(get_db)):
    return ServiceAuth(db).login(payload.email, payload.senha)


@router.get("/me", response_model=MeResponse)
def me(auth: AuthContext = Depends(get_current_user)):
    return {
        "id": auth.usuario.id,
        "nome": auth.usuario.nome,
        "email": auth.usuario.email,
        "ativo": auth.usuario.ativo,
        "perfil_id": auth.perfil.id,
        "perfil_nome": auth.perfil.nome,
    }
