from fastapi import FastAPI

from models.database import Base, engine
import models.ModelAluno
import models.ModelResponsavel
import models.ModelTurma
import models.ModelMatricula
import models.ModelNota
import models.ModelDisciplina
import models.ModelUsuario
import models.ModelPerfil
import models.ModelComunicado
import models.ModelFrequencia
import models.ModelMensalidade
import models.ModelPagamento
from routers.RouterAluno import router as aluno_router
from routers.RouterTurma import router as turma_router
from routers.RouterMatricula import router as matricula_router
from routers.RouterNota import router as nota_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ERP Escolar")

app.include_router(aluno_router)
app.include_router(turma_router)
app.include_router(matricula_router)
app.include_router(nota_router)
