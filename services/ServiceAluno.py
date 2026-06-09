from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.ModelFrequencia import ModelFrequencia
from models.ModelMatricula import ModelMatricula
from models.ModelMensalidade import ModelMensalidade
from models.ModelNota import ModelNota
from models.ModelPagamento import ModelPagamento
from repositories.RepositoryAluno import AlunoRepository
from schemas.SchemaAluno import AlunoCreate, AlunoUpdate


class ServiceAluno:
    def __init__(self, db: Session):
        self.repository = AlunoRepository(db)

    def criar(self, dados: AlunoCreate):
        if self.repository.get_by_cpf(dados.cpf):
            raise HTTPException(status_code=409, detail="CPF já cadastrado no sistema")
        if self.repository.get_by_matricula(dados.matricula_numero):
            raise HTTPException(status_code=409, detail="Número de matrícula já existe")
        return self.repository.create(dados)

    def buscar_por_id(self, aluno_id: int):
        aluno = self.repository.get_byID(aluno_id)
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        return aluno

    def listar(self):
        return self.repository.get_all()

    def atualizar(self, aluno_id: int, dados: AlunoUpdate):
        aluno = self.repository.update(aluno_id, dados)
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        return aluno

    def deletar(self, aluno_id: int):
        if not self.repository.get_byID(aluno_id):
            raise HTTPException(status_code=404, detail="Aluno não encontrado")

        db = self.repository.db

        # Apaga pagamentos vinculados às mensalidades do aluno
        mens_ids = [
            m.id for m in db.query(ModelMensalidade)
            .filter(ModelMensalidade.aluno_id == aluno_id).all()
        ]
        if mens_ids:
            db.query(ModelPagamento).filter(
                ModelPagamento.mensalidade_id.in_(mens_ids)
            ).delete(synchronize_session=False)

        db.query(ModelNota).filter(ModelNota.aluno_id == aluno_id).delete(synchronize_session=False)
        db.query(ModelFrequencia).filter(ModelFrequencia.aluno_id == aluno_id).delete(synchronize_session=False)
        db.query(ModelMensalidade).filter(ModelMensalidade.aluno_id == aluno_id).delete(synchronize_session=False)
        db.query(ModelMatricula).filter(ModelMatricula.aluno_id == aluno_id).delete(synchronize_session=False)
        db.commit()

        self.repository.delete(aluno_id)
        return {"mensagem": "Aluno deletado com sucesso"}
