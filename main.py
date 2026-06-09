import mimetypes
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware


class TrailingSlashMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Corrige /api/{recurso} → /api/{recurso}/ para todos os métodos
        # Só afeta paths com exatamente 3 segmentos (ex: /api/alunos)
        # Não afeta sub-rotas como /api/auth/login ou /api/alunos/123
        path = request.scope.get("path", "")
        segments = path.split("/")  # ['', 'api', 'recurso']
        if len(segments) == 3 and path.startswith("/api/") and not path.endswith("/"):
            request.scope["path"] = path + "/"
            request.scope["raw_path"] = (path + "/").encode()
        return await call_next(request)

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
from routers.RouterProfessor import router as professor_router
from routers.RouterUsuario import router as user_router
from routers.RouterSeed import router as seed_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ERP Escolar")

app.add_middleware(TrailingSlashMiddleware)
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
app.include_router(professor_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(seed_router, prefix="/api")

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
    if full_path.startswith("api/") or full_path == "api":
        raise HTTPException(status_code=404, detail="API endpoint not found")
    index = os.path.join(_DIST, "index.html")
    if not os.path.isfile(index):
        raise HTTPException(status_code=404, detail=f"index.html not found at {index}")
    with open(index, "rb") as f:
        return Response(content=f.read(), media_type="text/html")
