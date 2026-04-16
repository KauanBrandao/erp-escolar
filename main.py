from fastapi import FastAPI

from models.database import Base, engine
from routers.RouterAluno import router as aluno_router
from routers.RouterComunicado import router as comunicado_router
from routers.RouterDisciplina import router as disciplina_router
from routers.RouterFrequencia import router as frequencia_router
from routers.RouterMatricula import router as matricula_router
from routers.RouterMensalidade import router as mensalidade_router
from routers.RouterNota import router as nota_router
from routers.RouterPagamento import router as pagamento_router
from routers.RouterPerfil import router as perfil_router
from routers.RouterResponsavel import router as responsavel_router
from routers.RouterTurma import router as turma_router
from routers.RouterUsuario import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ERP Escolar")

app.include_router(aluno_router)
app.include_router(turma_router)
app.include_router(matricula_router)
app.include_router(nota_router)
app.include_router(comunicado_router)
app.include_router(disciplina_router)
app.include_router(frequencia_router)
app.include_router(mensalidade_router)
app.include_router(pagamento_router)
app.include_router(perfil_router)
app.include_router(responsavel_router)
app.include_router(user_router)
