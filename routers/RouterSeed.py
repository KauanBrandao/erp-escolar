"""
Endpoint temporário de seed — só pode ser chamado com o token de administrador.
POST /api/seed/professores
"""
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from core.auth_dependencies import require_permission
from core.database import SessionLocal, engine
from models.ModelDisciplina import ModelDisciplina
from models.ModelProfessor import ModelProfessor

router = APIRouter(prefix="/seed", tags=["Seed"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


PROFESSORES = [
    dict(nome="Ana Clara Oliveira",     cpf="111.111.111-01", email="ana.oliveira@escola.edu.br",      telefone="(11) 91111-0001", especialidade="Matemática"),
    dict(nome="Bruno Ferreira Lima",    cpf="111.111.111-02", email="bruno.lima@escola.edu.br",        telefone="(11) 91111-0002", especialidade="Língua Portuguesa"),
    dict(nome="Carla Souza Mendes",     cpf="111.111.111-03", email="carla.mendes@escola.edu.br",      telefone="(11) 91111-0003", especialidade="Ciências"),
    dict(nome="Diego Alves Costa",      cpf="111.111.111-04", email="diego.costa@escola.edu.br",       telefone="(11) 91111-0004", especialidade="História"),
    dict(nome="Eduarda Rocha Pinto",    cpf="111.111.111-05", email="eduarda.pinto@escola.edu.br",     telefone="(11) 91111-0005", especialidade="Geografia"),
    dict(nome="Felipe Nunes Barbosa",   cpf="111.111.111-06", email="felipe.barbosa@escola.edu.br",    telefone="(11) 91111-0006", especialidade="Educação Física"),
    dict(nome="Gabriela Torres Reis",   cpf="111.111.111-07", email="gabriela.reis@escola.edu.br",     telefone="(11) 91111-0007", especialidade="Artes"),
    dict(nome="Henrique Duarte Melo",   cpf="111.111.111-08", email="henrique.melo@escola.edu.br",     telefone="(11) 91111-0008", especialidade="Inglês"),
    dict(nome="Isabela Castro Viana",   cpf="111.111.111-09", email="isabela.viana@escola.edu.br",     telefone="(11) 91111-0009", especialidade="Física"),
    dict(nome="João Pedro Araújo",      cpf="111.111.111-10", email="joao.araujo@escola.edu.br",       telefone="(11) 91111-0010", especialidade="Química"),
    dict(nome="Karen Lima Santana",     cpf="111.111.111-11", email="karen.santana@escola.edu.br",     telefone="(11) 91111-0011", especialidade="Biologia"),
    dict(nome="Lucas Moreira Dias",     cpf="111.111.111-12", email="lucas.dias@escola.edu.br",        telefone="(11) 91111-0012", especialidade="Filosofia"),
    dict(nome="Mariana Cunha Lopes",    cpf="111.111.111-13", email="mariana.lopes@escola.edu.br",     telefone="(11) 91111-0013", especialidade="Sociologia"),
    dict(nome="Nicolas Teixeira Gomes", cpf="111.111.111-14", email="nicolas.gomes@escola.edu.br",    telefone="(11) 91111-0014", especialidade="Redação"),
    dict(nome="Olivia Pereira Franco",  cpf="111.111.111-15", email="olivia.franco@escola.edu.br",    telefone="(11) 91111-0015", especialidade="Literatura"),
    dict(nome="Paulo Ribeiro Cardoso",  cpf="111.111.111-16", email="paulo.cardoso@escola.edu.br",    telefone="(11) 91111-0016", especialidade="Informática"),
    dict(nome="Rafaela Monteiro Braga", cpf="111.111.111-17", email="rafaela.braga@escola.edu.br",    telefone="(11) 91111-0017", especialidade="Religião"),
    dict(nome="Sérgio Azevedo Nogueira",cpf="111.111.111-18", email="sergio.nogueira@escola.edu.br",  telefone="(11) 91111-0018", especialidade="Espanhol"),
]

KEYWORD_MAP = {
    "matemática": "Matemática", "matematica": "Matemática", "mat": "Matemática",
    "português": "Língua Portuguesa", "portugues": "Língua Portuguesa",
    "língua": "Língua Portuguesa", "lingua": "Língua Portuguesa",
    "redação": "Redação", "redacao": "Redação",
    "literatura": "Literatura",
    "ciências": "Ciências", "ciencias": "Ciências", "ciencia": "Ciências",
    "história": "História", "historia": "História",
    "geografia": "Geografia",
    "física": "Física", "fisica": "Física",
    "química": "Química", "quimica": "Química",
    "biologia": "Biologia",
    "filosofia": "Filosofia",
    "sociologia": "Sociologia",
    "inglês": "Inglês", "ingles": "Inglês",
    "espanhol": "Espanhol",
    "educação física": "Educação Física", "ed. física": "Educação Física", "edfisica": "Educação Física",
    "artes": "Artes", "arte": "Artes",
    "informática": "Informática", "informatica": "Informática",
    "religião": "Religião", "religiao": "Religião",
}


def _match(disc_nome: str) -> str:
    lower = disc_nome.lower()
    for kw, esp in KEYWORD_MAP.items():
        if kw in lower:
            return esp
    return "Ciências"


@router.post("/professores")
def seed_professores(
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("*")),
):
    # 1. Garante coluna professor_id em Disciplinas
    with engine.connect() as conn:
        conn.execute(text(
            'ALTER TABLE "Disciplinas" ADD COLUMN IF NOT EXISTS professor_id INTEGER REFERENCES "Professores"(id)'
        ))
        conn.commit()

    # 2. Cria professores
    esp_map: dict[str, ModelProfessor] = {}
    criados = 0
    for p in PROFESSORES:
        existing = db.query(ModelProfessor).filter(ModelProfessor.cpf == p["cpf"]).first()
        if existing:
            esp_map[p["especialidade"]] = existing
            continue
        prof = ModelProfessor(
            nome=p["nome"], cpf=p["cpf"], email=p["email"],
            telefone=p["telefone"], especialidade=p["especialidade"],
            ativo=True, criado_em=date.today(),
        )
        db.add(prof)
        db.flush()
        esp_map[p["especialidade"]] = prof
        criados += 1
    db.commit()

    # Recarrega com IDs
    for p in PROFESSORES:
        prof = db.query(ModelProfessor).filter(ModelProfessor.cpf == p["cpf"]).first()
        if prof:
            esp_map[p["especialidade"]] = prof

    # 3. Vincula disciplinas
    disciplinas = db.query(ModelDisciplina).all()
    vinculadas = 0
    for disc in disciplinas:
        esp = _match(disc.nome)
        prof = esp_map.get(esp) or esp_map.get("Ciências")
        if prof and disc.professor_id != prof.id:
            disc.professor_id = prof.id
            vinculadas += 1
    db.commit()

    return {
        "professores_criados": criados,
        "disciplinas_vinculadas": vinculadas,
    }
