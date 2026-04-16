from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.database import SessionLocal
from services.ServiceMatricula import ServiceMatricula
from schemas.SchemaMatricula import MatriculaCreate, MatriculaResponse, MatriculaUpdate

router = APIRouter(prefix="/matriculas", tags=["Matrículas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=MatriculaResponse, status_code=201)
def criar_matricula(dados: MatriculaCreate, db: Session = Depends(get_db)):
    return ServiceMatricula(db).criar(dados)


@router.get("/", response_model=list[MatriculaResponse])
def listar_matriculas(db: Session = Depends(get_db)):
    return ServiceMatricula(db).listar()


@router.get("/{matricula_id}", response_model=MatriculaResponse)
def buscar_matricula(matricula_id: int, db: Session = Depends(get_db)):
    return ServiceMatricula(db).buscar_por_id(matricula_id)


@router.put("/{matricula_id}", response_model=MatriculaResponse)
def atualizar_matricula(matricula_id: int, dados: MatriculaUpdate, db: Session = Depends(get_db)):
    return ServiceMatricula(db).atualizar(matricula_id, dados)


@router.delete("/{matricula_id}")
def deletar_matricula(matricula_id: int, db: Session = Depends(get_db)):
    return ServiceMatricula(db).deletar(matricula_id)
