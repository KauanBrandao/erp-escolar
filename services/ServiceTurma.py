from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.ModelDisciplina import ModelDisciplina
from models.ModelFrequencia import ModelFrequencia
from models.ModelMatricula import ModelMatricula
from models.ModelNota import ModelNota
from repositories.RepositoryTurma import TurmaRepository
from schemas.SchemaTurma import TurmaCreate, TurmaUpdate


class ServiceTurma:
    def __init__(self, db: Session):
        self.repository = TurmaRepository(db)

    def criar(self, dados: TurmaCreate):
        return self.repository.create(dados)

    def buscar_por_id(self, turma_id: int):
        turma = self.repository.get_byID(turma_id)
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        return turma

    def listar(self):
        return self.repository.get_all()

    def atualizar(self, turma_id: int, dados: TurmaUpdate):
        turma = self.repository.update(turma_id, dados)
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        return turma

    def deletar(self, turma_id: int):
        if not self.repository.get_byID(turma_id):
            raise HTTPException(status_code=404, detail="Turma não encontrada")

        db = self.repository.db

        # Disciplinas desta turma
        disc_ids = [
            d.id for d in db.query(ModelDisciplina)
            .filter(ModelDisciplina.turma_id == turma_id).all()
        ]

        if disc_ids:
            db.query(ModelNota).filter(
                ModelNota.disciplina_id.in_(disc_ids)
            ).delete(synchronize_session=False)
            db.query(ModelFrequencia).filter(
                ModelFrequencia.disciplina_id.in_(disc_ids)
            ).delete(synchronize_session=False)
            db.query(ModelDisciplina).filter(
                ModelDisciplina.turma_id == turma_id
            ).delete(synchronize_session=False)

        db.query(ModelMatricula).filter(
            ModelMatricula.turma_id == turma_id
        ).delete(synchronize_session=False)

        db.commit()

        self.repository.delete(turma_id)
        return {"mensagem": "Turma deletada com sucesso"}
