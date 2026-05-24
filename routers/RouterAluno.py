from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.auth_dependencies import require_permission
from core.database import SessionLocal
from schemas.SchemaAluno import AlunoCreate, AlunoResponse, AlunoUpdate
from services.ServiceAluno import ServiceAluno

router = APIRouter(prefix="/alunos", tags=["Alunos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=AlunoResponse, status_code=201)
def criar_aluno(
    dados: AlunoCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("alunos:write")),
):
    return ServiceAluno(db).criar(dados)


@router.get("/", response_model=list[AlunoResponse])
def listar_alunos(
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("alunos:read")),
):
    return ServiceAluno(db).listar()


@router.get("/{aluno_id}", response_model=AlunoResponse)
def buscar_aluno(
    aluno_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("alunos:read")),
):
    return ServiceAluno(db).buscar_por_id(aluno_id)


@router.put("/{aluno_id}", response_model=AlunoResponse)
def atualizar_aluno(
    aluno_id: int,
    dados: AlunoUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("alunos:write")),
):
    return ServiceAluno(db).atualizar(aluno_id, dados)


@router.delete("/{aluno_id}")
def deletar_aluno(
    aluno_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("alunos:write")),
):
    return ServiceAluno(db).deletar(aluno_id)
