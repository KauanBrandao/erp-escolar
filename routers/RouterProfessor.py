from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.auth_dependencies import require_permission
from core.database import SessionLocal
from schemas.SchemaProfessor import ProfessorCreate, ProfessorResponse, ProfessorUpdate
from services.ServiceProfessor import ServiceProfessor

router = APIRouter(prefix="/professores", tags=["Professores"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ProfessorResponse, status_code=201)
def criar_professor(
    dados: ProfessorCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("professores:write")),
):
    return ServiceProfessor(db).criar(dados)


@router.get("/", response_model=list[ProfessorResponse])
def listar_professores(
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("professores:read")),
):
    return ServiceProfessor(db).listar()


@router.get("/{professor_id}", response_model=ProfessorResponse)
def buscar_professor(
    professor_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("professores:read")),
):
    return ServiceProfessor(db).buscar_por_id(professor_id)


@router.put("/{professor_id}", response_model=ProfessorResponse)
def atualizar_professor(
    professor_id: int,
    dados: ProfessorUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("professores:write")),
):
    return ServiceProfessor(db).atualizar(professor_id, dados)


@router.delete("/{professor_id}")
def deletar_professor(
    professor_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("professores:write")),
):
    return ServiceProfessor(db).deletar(professor_id)
