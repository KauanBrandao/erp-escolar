import calendar
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.ModelMensalidade import ModelMensalidade
from repositories.RepositoryMatricula import MatriculaRepository
from repositories.RepositoryAluno import AlunoRepository
from repositories.RepositoryTurma import TurmaRepository
from schemas.SchemaMatricula import MatriculaCreate, MatriculaUpdate


class ServiceMatricula:
    def __init__(self, db: Session):
        self.repository = MatriculaRepository(db)
        self.aluno_repo = AlunoRepository(db)
        self.turma_repo = TurmaRepository(db)
        self.db = db

    def criar(self, dados: MatriculaCreate):
        if not self.aluno_repo.get_byID(dados.aluno_id):
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        turma = self.turma_repo.get_byID(dados.turma_id)
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")

        matricula = self.repository.create(dados)

        # Gera 12 mensalidades automáticas para o ano letivo da turma
        if dados.valor_mensalidade and dados.valor_mensalidade > 0:
            ano = turma.ano_letivo
            for mes in range(1, 13):
                dia_venc = min(10, calendar.monthrange(ano, mes)[1])
                mens = ModelMensalidade(
                    aluno_id=dados.aluno_id,
                    mes=mes,
                    ano=ano,
                    valor=dados.valor_mensalidade,
                    vencimento=date(ano, mes, dia_venc),
                    status="ativa",
                )
                self.db.add(mens)
            self.db.commit()

        return matricula

    def buscar_por_id(self, matricula_id: int):
        matricula = self.repository.get_byID(matricula_id)
        if not matricula:
            raise HTTPException(status_code=404, detail="Matrícula não encontrada")
        return matricula

    def listar(self):
        return self.repository.get_all()

    def atualizar(self, matricula_id: int, dados: MatriculaUpdate):
        matricula = self.repository.update(matricula_id, dados)
        if not matricula:
            raise HTTPException(status_code=404, detail="Matrícula não encontrada")
        return matricula

    def deletar(self, matricula_id: int):
        sucesso = self.repository.delete(matricula_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Matrícula não encontrada")
        return {"mensagem": "Matrícula deletada com sucesso"}
