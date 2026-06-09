"""
Seed: cria professores fictícios e os vincula a todas as disciplinas existentes.

Como rodar:
    cd erp-escolar
    python -m scripts.seed_professores

O script:
  1. Garante que a coluna professor_id existe em Disciplinas (via ALTER TABLE).
  2. Cria professores fictícios com base nos nomes das disciplinas.
  3. Associa cada disciplina ao professor cuja especialidade combina.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date
from sqlalchemy import text
from core.database import SessionLocal, engine
from models.ModelProfessor import ModelProfessor
from models.ModelDisciplina import ModelDisciplina

# ---------------------------------------------------------------------------
# Professores fictícios — um por área de conhecimento
# ---------------------------------------------------------------------------
PROFESSORES = [
    dict(nome="Ana Clara Oliveira",    cpf="111.111.111-01", email="ana.oliveira@escola.edu.br",     telefone="(11) 91111-0001", especialidade="Matemática"),
    dict(nome="Bruno Ferreira Lima",   cpf="111.111.111-02", email="bruno.lima@escola.edu.br",       telefone="(11) 91111-0002", especialidade="Língua Portuguesa"),
    dict(nome="Carla Souza Mendes",    cpf="111.111.111-03", email="carla.mendes@escola.edu.br",     telefone="(11) 91111-0003", especialidade="Ciências"),
    dict(nome="Diego Alves Costa",     cpf="111.111.111-04", email="diego.costa@escola.edu.br",      telefone="(11) 91111-0004", especialidade="História"),
    dict(nome="Eduarda Rocha Pinto",   cpf="111.111.111-05", email="eduarda.pinto@escola.edu.br",    telefone="(11) 91111-0005", especialidade="Geografia"),
    dict(nome="Felipe Nunes Barbosa",  cpf="111.111.111-06", email="felipe.barbosa@escola.edu.br",   telefone="(11) 91111-0006", especialidade="Educação Física"),
    dict(nome="Gabriela Torres Reis",  cpf="111.111.111-07", email="gabriela.reis@escola.edu.br",    telefone="(11) 91111-0007", especialidade="Artes"),
    dict(nome="Henrique Duarte Melo",  cpf="111.111.111-08", email="henrique.melo@escola.edu.br",    telefone="(11) 91111-0008", especialidade="Inglês"),
    dict(nome="Isabela Castro Viana",  cpf="111.111.111-09", email="isabela.viana@escola.edu.br",    telefone="(11) 91111-0009", especialidade="Física"),
    dict(nome="João Pedro Araújo",     cpf="111.111.111-10", email="joao.araujo@escola.edu.br",      telefone="(11) 91111-0010", especialidade="Química"),
    dict(nome="Karen Lima Santana",    cpf="111.111.111-11", email="karen.santana@escola.edu.br",    telefone="(11) 91111-0011", especialidade="Biologia"),
    dict(nome="Lucas Moreira Dias",    cpf="111.111.111-12", email="lucas.dias@escola.edu.br",       telefone="(11) 91111-0012", especialidade="Filosofia"),
    dict(nome="Mariana Cunha Lopes",   cpf="111.111.111-13", email="mariana.lopes@escola.edu.br",    telefone="(11) 91111-0013", especialidade="Sociologia"),
    dict(nome="Nicolas Teixeira Gomes",cpf="111.111.111-14", email="nicolas.gomes@escola.edu.br",   telefone="(11) 91111-0014", especialidade="Redação"),
    dict(nome="Olivia Pereira Franco", cpf="111.111.111-15", email="olivia.franco@escola.edu.br",   telefone="(11) 91111-0015", especialidade="Literatura"),
    dict(nome="Paulo Ribeiro Cardoso", cpf="111.111.111-16", email="paulo.cardoso@escola.edu.br",   telefone="(11) 91111-0016", especialidade="Informática"),
    dict(nome="Rafaela Monteiro Braga",cpf="111.111.111-17", email="rafaela.braga@escola.edu.br",   telefone="(11) 91111-0017", especialidade="Religião"),
    dict(nome="Sérgio Azevedo Nogueira",cpf="111.111.111-18",email="sergio.nogueira@escola.edu.br", telefone="(11) 91111-0018", especialidade="Espanhol"),
]

# Mapeamento palavra-chave → especialidade para vincular disciplinas
KEYWORD_MAP = {
    "matemática": "Matemática",
    "matematica": "Matemática",
    "mat":        "Matemática",
    "português":  "Língua Portuguesa",
    "portugues":  "Língua Portuguesa",
    "língua":     "Língua Portuguesa",
    "lingua":     "Língua Portuguesa",
    "redação":    "Redação",
    "redacao":    "Redação",
    "literatura": "Literatura",
    "ciências":   "Ciências",
    "ciencias":   "Ciências",
    "ciencia":    "Ciências",
    "história":   "História",
    "historia":   "História",
    "geografia":  "Geografia",
    "geo":        "Geografia",
    "física":     "Física",
    "fisica":     "Física",
    "química":    "Química",
    "quimica":    "Química",
    "biologia":   "Biologia",
    "bio":        "Biologia",
    "filosofia":  "Filosofia",
    "sociologia": "Sociologia",
    "sociolog":   "Sociologia",
    "inglês":     "Inglês",
    "ingles":     "Inglês",
    "english":    "Inglês",
    "espanhol":   "Espanhol",
    "spanish":    "Espanhol",
    "educação física": "Educação Física",
    "ed. física": "Educação Física",
    "ed.fisica":  "Educação Física",
    "edfisica":   "Educação Física",
    "artes":      "Artes",
    "arte":       "Artes",
    "informática":"Informática",
    "informatica":"Informática",
    "religião":   "Religião",
    "religiao":   "Religião",
}

DEFAULT_ESPECIALIDADE = "Ciências"  # fallback


def match_especialidade(disc_nome: str) -> str:
    lower = disc_nome.lower()
    for kw, esp in KEYWORD_MAP.items():
        if kw in lower:
            return esp
    return DEFAULT_ESPECIALIDADE


def ensure_column_exists(engine):
    """Adiciona professor_id em Disciplinas se ainda não existir (idempotente)."""
    with engine.connect() as conn:
        # Supabase/PostgreSQL
        result = conn.execute(text("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'Disciplinas' AND column_name = 'professor_id'
        """))
        if result.fetchone() is None:
            print("→ Adicionando coluna professor_id em Disciplinas...")
            conn.execute(text(
                'ALTER TABLE "Disciplinas" ADD COLUMN professor_id INTEGER REFERENCES "Professores"(id)'
            ))
            conn.commit()
            print("  Coluna adicionada.")
        else:
            print("→ Coluna professor_id já existe em Disciplinas.")


def run():
    ensure_column_exists(engine)

    db = SessionLocal()
    try:
        # 1. Criar professores (pula se CPF/email já existe)
        esp_to_professor: dict[str, ModelProfessor] = {}
        created = 0
        for p in PROFESSORES:
            existing = db.query(ModelProfessor).filter(ModelProfessor.cpf == p["cpf"]).first()
            if existing:
                esp_to_professor[p["especialidade"]] = existing
                continue
            prof = ModelProfessor(
                nome=p["nome"],
                cpf=p["cpf"],
                email=p["email"],
                telefone=p["telefone"],
                especialidade=p["especialidade"],
                ativo=True,
                criado_em=date.today(),
            )
            db.add(prof)
            db.flush()
            esp_to_professor[p["especialidade"]] = prof
            created += 1

        db.commit()
        print(f"→ {created} professores criados ({len(PROFESSORES) - created} já existiam).")

        # Recarrega mapa com IDs definitivos
        for p in PROFESSORES:
            prof = db.query(ModelProfessor).filter(ModelProfessor.cpf == p["cpf"]).first()
            if prof:
                esp_to_professor[p["especialidade"]] = prof

        # 2. Vincular disciplinas
        disciplinas = db.query(ModelDisciplina).all()
        linked = 0
        for disc in disciplinas:
            esp = match_especialidade(disc.nome)
            prof = esp_to_professor.get(esp) or esp_to_professor.get(DEFAULT_ESPECIALIDADE)
            if prof and disc.professor_id != prof.id:
                disc.professor_id = prof.id
                linked += 1

        db.commit()
        print(f"→ {linked} disciplinas vinculadas a professores.")
        print("Seed concluído com sucesso!")

    finally:
        db.close()


if __name__ == "__main__":
    run()
