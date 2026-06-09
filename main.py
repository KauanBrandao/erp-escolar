import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from core.database import Base, engine
from routers.RouterAluno import router as aluno_router
from routers.RouterAuth import router as auth_router
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

#Configurar para a url do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(auth_router)
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

_DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "dist")

@app.get("/assets/{file_path:path}", include_in_schema=False)
def serve_assets(file_path: str):
    full = os.path.join(_DIST, "assets", file_path)
    if os.path.isfile(full):
        return FileResponse(full)
    raise HTTPException(status_code=404)

@app.get("/{full_path:path}", include_in_schema=False)
def serve_frontend(full_path: str):
    return FileResponse(os.path.join(_DIST, "index.html"))
