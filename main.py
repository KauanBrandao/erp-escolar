from fastapi import FastAPI
from routers.RouterAluno import router as aluno_router

app = FastAPI(title="ERP Escolar")

app.include_router(aluno_router)

@app.get("/")
def home():
    return {"mensagem": "API ERP Escolar funcionando"}