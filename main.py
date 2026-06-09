import mimetypes
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

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




app.include_router(auth_router, prefix="/api")
app.include_router(aluno_router, prefix="/api")
app.include_router(turma_router, prefix="/api")
app.include_router(matricula_router, prefix="/api")
app.include_router(nota_router, prefix="/api")
app.include_router(comunicado_router, prefix="/api")
app.include_router(disciplina_router, prefix="/api")
app.include_router(frequencia_router, prefix="/api")
app.include_router(mensalidade_router, prefix="/api")
app.include_router(pagamento_router, prefix="/api")
app.include_router(perfil_router, prefix="/api")
app.include_router(responsavel_router, prefix="/api")
app.include_router(user_router, prefix="/api")

_DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "dist")

@app.get("/assets/{file_path:path}", include_in_schema=False)
def serve_assets(file_path: str):
    full = os.path.join(_DIST, "assets", file_path)
    if not os.path.isfile(full):
        raise HTTPException(status_code=404)
    mime_type, _ = mimetypes.guess_type(full)
    with open(full, "rb") as f:
        return Response(content=f.read(), media_type=mime_type or "application/octet-stream")

@app.get("/{full_path:path}", include_in_schema=False)
def serve_frontend(full_path: str):
    index = os.path.join(_DIST, "index.html")
    if not os.path.isfile(index):
        raise HTTPException(status_code=404, detail=f"index.html not found at {index}")
    with open(index, "rb") as f:
        return Response(content=f.read(), media_type="text/html")
