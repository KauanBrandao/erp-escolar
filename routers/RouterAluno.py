from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import SessionLocal
from services.ServiceAluno import ServiceAluno
from schemas.SchemaAluno import AlunoCreate, AlunoResponse, AlunoUpdate

router = APIRouter(prefix="/alunos", tags=["Alunos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AlunoResponse)
def criar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    service = ServiceAluno(db)
    return service.create(aluno)

@router.get("/", response_model=list[AlunoResponse])
def listar_alunos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = ServiceAluno(db)
    return service.get_all(skip, limit)

@router.get("/{aluno_id}", response_model=AlunoResponse)
def buscar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    service = ServiceAluno(db)
    aluno = service.get_by_id(aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@router.put("/{aluno_id}", response_model=AlunoResponse)
def atualizar_aluno(aluno_id: int, aluno_data: AlunoUpdate, db: Session = Depends(get_db)):
    service = ServiceAluno(db)
    aluno = service.update(aluno_id, aluno_data)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@router.delete("/{aluno_id}")
def deletar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    service = ServiceAluno(db)
    sucesso = service.delete(aluno_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return {"message": "Aluno removido com sucesso"}