"""
Script de seed para popular o banco Supabase com dados realistas.
Execute: python seed.py
"""
import os
import sys
import random
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()

from core.database import SessionLocal, engine, Base
from models.ModelPerfil import ModelPerfil
from models.ModelUsuario import ModelUsuario
from models.ModelResponsavel import ModelResponsavel
from models.ModelAluno import ModelAluno
from models.ModelTurma import ModelTurma
from models.ModelDisciplina import ModelDisciplina
from models.ModelMatricula import ModelMatricula
from models.ModelNota import ModelNota
from models.ModelFrequencia import ModelFrequencia
from models.ModelMensalidade import ModelMensalidade
from models.ModelPagamento import ModelPagamento
from models.ModelComunicado import ModelComunicado

import bcrypt


def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def main():
    print("Criando tabelas...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # ── 1. PERFIS ────────────────────────────────────────────────
        print("Inserindo perfis...")
        perfis_data = [
            ("administrador",          "Acesso total ao sistema"),
            ("secretaria",             "Gestão de alunos e matrículas"),
            ("coordenacao_pedagogica", "Gestão pedagógica e notas"),
            ("financeiro",             "Gestão financeira e mensalidades"),
            ("responsavel",            "Acesso do responsável pelo aluno"),
        ]
        perfis = {}
        for nome, desc in perfis_data:
            p = db.query(ModelPerfil).filter_by(nome=nome).first()
            if not p:
                p = ModelPerfil(nome=nome, descricao=desc)
                db.add(p)
                db.flush()
            perfis[nome] = p
        db.commit()
        print(f"  {len(perfis)} perfis OK")

        # ── 2. USUÁRIOS ───────────────────────────────────────────────
        print("Inserindo usuários...")
        usuarios_data = [
            ("Administrador",           "admin@escola.com",      "admin123",   "administrador"),
            ("Maria Secretaria",        "secretaria@escola.com", "sec123",     "secretaria"),
            ("Prof. Carlos Coord.",     "coord@escola.com",      "coord123",   "coordenacao_pedagogica"),
            ("Ana Financeiro",          "financeiro@escola.com", "fin123",     "financeiro"),
            ("Roberto Responsável",     "responsavel@escola.com","resp123",    "responsavel"),
            ("Fernanda Secretaria",     "fernanda@escola.com",   "fern123",    "secretaria"),
        ]
        usuarios = {}
        for nome, email, senha, perfil_nome in usuarios_data:
            u = db.query(ModelUsuario).filter_by(email=email).first()
            if not u:
                u = ModelUsuario(
                    nome=nome,
                    email=email,
                    senha_hash=hash_senha(senha),
                    ativo=True,
                    criado_em=date(2024, 1, 15),
                    perfil_id=perfis[perfil_nome].id,
                )
                db.add(u)
                db.flush()
            usuarios[email] = u
        db.commit()
        print(f"  {len(usuarios)} usuários OK")

        # ── 3. TURMAS ─────────────────────────────────────────────────
        print("Inserindo turmas...")
        turmas_data = [
            ("6º Ano A", "6º Ano", "Manhã",  2025),
            ("6º Ano B", "6º Ano", "Tarde",  2025),
            ("7º Ano A", "7º Ano", "Manhã",  2025),
            ("7º Ano B", "7º Ano", "Tarde",  2025),
            ("8º Ano A", "8º Ano", "Manhã",  2025),
            ("8º Ano B", "8º Ano", "Tarde",  2025),
            ("9º Ano A", "9º Ano", "Manhã",  2025),
            ("9º Ano B", "9º Ano", "Tarde",  2025),
        ]
        turmas = []
        for nome, serie, turno, ano in turmas_data:
            t = db.query(ModelTurma).filter_by(nome=nome, ano_letivo=ano).first()
            if not t:
                t = ModelTurma(
                    nome=nome,
                    serie=serie,
                    turno=turno,
                    ano_letivo=ano,
                    perfil_id=perfis["coordenacao_pedagogica"].id,
                )
                db.add(t)
                db.flush()
            turmas.append(t)
        db.commit()
        print(f"  {len(turmas)} turmas OK")

        # ── 4. DISCIPLINAS ────────────────────────────────────────────
        print("Inserindo disciplinas...")
        disc_base = [
            ("Matemática",          "MAT", 80),
            ("Língua Portuguesa",   "POR", 80),
            ("Ciências",            "CIE", 60),
            ("História",            "HIS", 60),
            ("Geografia",           "GEO", 60),
            ("Inglês",              "ING", 40),
            ("Educação Física",     "EDF", 40),
            ("Artes",               "ART", 40),
        ]
        disciplinas = {}  # turma_id -> list of disciplinas
        for turma in turmas:
            disciplinas[turma.id] = []
            for nome, cod_base, ch in disc_base:
                cod = f"{cod_base}-{turma.nome.replace(' ', '').replace('º', '')}"
                d = db.query(ModelDisciplina).filter_by(codigo=cod).first()
                if not d:
                    d = ModelDisciplina(
                        nome=nome,
                        codigo=cod,
                        carga_horaria=ch,
                        turma_id=turma.id,
                    )
                    db.add(d)
                    db.flush()
                disciplinas[turma.id].append(d)
        db.commit()
        print(f"  {sum(len(v) for v in disciplinas.values())} disciplinas OK")

        # ── 5. RESPONSÁVEIS ───────────────────────────────────────────
        print("Inserindo responsáveis...")
        responsaveis_data = [
            ("José Carlos Silva",     "111.222.333-01", "(11) 99001-0001", "jose.silva@gmail.com"),
            ("Ana Paula Souza",       "111.222.333-02", "(11) 99001-0002", "ana.souza@gmail.com"),
            ("Marcos Pereira",        "111.222.333-03", "(11) 99001-0003", "marcos.pereira@gmail.com"),
            ("Fernanda Costa",        "111.222.333-04", "(11) 99001-0004", "fernanda.costa@gmail.com"),
            ("Ricardo Almeida",       "111.222.333-05", "(11) 99001-0005", "ricardo.almeida@gmail.com"),
            ("Cláudia Nascimento",    "111.222.333-06", "(11) 99001-0006", "claudia.nasc@gmail.com"),
            ("Sérgio Lima",           "111.222.333-07", "(11) 99001-0007", "sergio.lima@gmail.com"),
            ("Patrícia Ferreira",     "111.222.333-08", "(11) 99001-0008", "patricia.ferr@gmail.com"),
            ("Eduardo Santos",        "111.222.333-09", "(11) 99001-0009", "eduardo.santos@gmail.com"),
            ("Luciana Oliveira",      "111.222.333-10", "(11) 99001-0010", "luciana.oli@gmail.com"),
            ("Antônio Carvalho",      "111.222.333-11", "(11) 99001-0011", "antonio.carv@gmail.com"),
            ("Mariana Rodrigues",     "111.222.333-12", "(11) 99001-0012", "mariana.rod@gmail.com"),
            ("Felipe Martins",        "111.222.333-13", "(11) 99001-0013", "felipe.mart@gmail.com"),
            ("Juliana Castro",        "111.222.333-14", "(11) 99001-0014", "juliana.cast@gmail.com"),
            ("Bruno Gomes",           "111.222.333-15", "(11) 99001-0015", "bruno.gomes@gmail.com"),
            ("Aline Barbosa",         "111.222.333-16", "(11) 99001-0016", "aline.barb@gmail.com"),
            ("Wagner Araújo",         "111.222.333-17", "(11) 99001-0017", "wagner.araujo@gmail.com"),
            ("Simone Teixeira",       "111.222.333-18", "(11) 99001-0018", "simone.teix@gmail.com"),
            ("Henrique Pinto",        "111.222.333-19", "(11) 99001-0019", "henrique.pint@gmail.com"),
            ("Tatiana Moreira",       "111.222.333-20", "(11) 99001-0020", "tatiana.mor@gmail.com"),
            ("Gustavo Ribeiro",       "111.222.333-21", "(11) 99001-0021", "gustavo.rib@gmail.com"),
            ("Vanessa Monteiro",      "111.222.333-22", "(11) 99001-0022", "vanessa.mont@gmail.com"),
            ("Alexandre Campos",      "111.222.333-23", "(11) 99001-0023", "alexandre.cam@gmail.com"),
            ("Carla Cunha",           "111.222.333-24", "(11) 99001-0024", "carla.cunha@gmail.com"),
        ]
        responsaveis = []
        for nome, cpf, tel, email in responsaveis_data:
            r = db.query(ModelResponsavel).filter_by(cpf=cpf).first()
            if not r:
                r = ModelResponsavel(
                    nome=nome,
                    cpf=cpf,
                    telefone=tel,
                    email=email,
                    parentesco=None,
                )
                db.add(r)
                db.flush()
            responsaveis.append(r)
        db.commit()
        print(f"  {len(responsaveis)} responsáveis OK")

        # ── 6. ALUNOS ─────────────────────────────────────────────────
        print("Inserindo alunos...")
        alunos_data = [
            # (nome, cpf, telefone, matricula, nascimento, responsavel_idx)
            ("Lucas Silva",          "222.333.444-01", "(11) 98000-0001", 20250001, date(2012, 3, 14), 0),
            ("Beatriz Souza",        "222.333.444-02", "(11) 98000-0002", 20250002, date(2012, 7, 22), 1),
            ("Enzo Pereira",         "222.333.444-03", "(11) 98000-0003", 20250003, date(2013, 1,  5), 2),
            ("Sophia Costa",         "222.333.444-04", "(11) 98000-0004", 20250004, date(2013, 9, 17), 3),
            ("Matheus Almeida",      "222.333.444-05", "(11) 98000-0005", 20250005, date(2011, 5, 30), 4),
            ("Isabella Nascimento",  "222.333.444-06", "(11) 98000-0006", 20250006, date(2011,11, 12), 5),
            ("Gabriel Lima",         "222.333.444-07", "(11) 98000-0007", 20250007, date(2010, 4,  8), 6),
            ("Larissa Ferreira",     "222.333.444-08", "(11) 98000-0008", 20250008, date(2010, 8, 25), 7),
            ("Pedro Santos",         "222.333.444-09", "(11) 98000-0009", 20250009, date(2009, 2, 19), 8),
            ("Valentina Oliveira",   "222.333.444-10", "(11) 98000-0010", 20250010, date(2009, 6,  3), 9),
            ("Davi Carvalho",        "222.333.444-11", "(11) 98000-0011", 20250011, date(2012,10, 11), 10),
            ("Manuela Rodrigues",    "222.333.444-12", "(11) 98000-0012", 20250012, date(2013, 3, 28), 11),
            ("Arthur Martins",       "222.333.444-13", "(11) 98000-0013", 20250013, date(2011, 7, 16), 12),
            ("Laura Castro",         "222.333.444-14", "(11) 98000-0014", 20250014, date(2011,12,  2), 13),
            ("Samuel Gomes",         "222.333.444-15", "(11) 98000-0015", 20250015, date(2010, 1, 20), 14),
            ("Helena Barbosa",       "222.333.444-16", "(11) 98000-0016", 20250016, date(2009, 5,  9), 15),
            ("Cauã Araújo",          "222.333.444-17", "(11) 98000-0017", 20250017, date(2012, 8,  4), 16),
            ("Alice Teixeira",       "222.333.444-18", "(11) 98000-0018", 20250018, date(2013, 2, 14), 17),
            ("Theo Pinto",           "222.333.444-19", "(11) 98000-0019", 20250019, date(2010, 9, 27), 18),
            ("Cecília Moreira",      "222.333.444-20", "(11) 98000-0020", 20250020, date(2009, 3,  6), 19),
            ("Rafael Ribeiro",       "222.333.444-21", "(11) 98000-0021", 20250021, date(2012, 5, 21), 20),
            ("Lívia Monteiro",       "222.333.444-22", "(11) 98000-0022", 20250022, date(2013, 7,  1), 21),
            ("Nicolas Campos",       "222.333.444-23", "(11) 98000-0023", 20250023, date(2011, 4, 18), 22),
            ("Isadora Cunha",        "222.333.444-24", "(11) 98000-0024", 20250024, date(2010,11, 30), 23),
        ]
        alunos = []
        for nome, cpf, tel, mat, nasc, resp_idx in alunos_data:
            a = db.query(ModelAluno).filter_by(cpf=cpf).first()
            if not a:
                a = ModelAluno(
                    nome=nome,
                    cpf=cpf,
                    telefone=tel,
                    matricula_numero=mat,
                    ativo=True,
                    data_nascimento=nasc,
                    criado_em=date(2025, 1, 20),
                    responsavel_id=responsaveis[resp_idx].id,
                )
                db.add(a)
                db.flush()
            alunos.append(a)
        db.commit()
        print(f"  {len(alunos)} alunos OK")

        # ── 7. MATRÍCULAS ─────────────────────────────────────────────
        # Distribuir 3 alunos por turma (8 turmas × 3 = 24)
        print("Inserindo matrículas...")
        turma_dist = [
            (0, [0, 1, 2]),    # 6ºA: Lucas, Beatriz, Enzo
            (1, [3, 4, 5]),    # 6ºB: Sophia, Matheus, Isabella
            (2, [6, 7, 8]),    # 7ºA: Gabriel, Larissa, Pedro
            (3, [9, 10, 11]),  # 7ºB: Valentina, Davi, Manuela
            (4, [12, 13, 14]), # 8ºA: Arthur, Laura, Samuel
            (5, [15, 16, 17]), # 8ºB: Helena, Cauã, Alice
            (6, [18, 19, 20]), # 9ºA: Theo, Cecília, Rafael
            (7, [21, 22, 23]), # 9ºB: Lívia, Nicolas, Isadora
        ]
        matriculas_map = {}  # aluno_id -> turma
        for turma_idx, aluno_idxs in turma_dist:
            turma = turmas[turma_idx]
            for ai in aluno_idxs:
                aluno = alunos[ai]
                m = db.query(ModelMatricula).filter_by(
                    aluno_id=aluno.id, turma_id=turma.id
                ).first()
                if not m:
                    m = ModelMatricula(
                        aluno_id=aluno.id,
                        turma_id=turma.id,
                        data_matricula=date(2025, 1, 20),
                        status="ativa",
                        observacao=None,
                    )
                    db.add(m)
                    db.flush()
                matriculas_map[aluno.id] = turma
        db.commit()
        print(f"  {len(matriculas_map)} matrículas OK")

        # ── 8. NOTAS ─────────────────────────────────────────────────
        # Boletim completo: prova + trabalho + recuperacao por bimestre
        print("Inserindo notas (boletim completo ano letivo 2025)...")
        random.seed(42)
        notas_count = 0
        bimestre_dates = {
            1: date(2025, 3, 20),
            2: date(2025, 5, 30),
            3: date(2025, 8, 25),
            4: date(2025, 10, 30),
        }

        for turma_idx, aluno_idxs in turma_dist:
            turma = turmas[turma_idx]
            discs = disciplinas[turma.id]
            for ai in aluno_idxs:
                aluno = alunos[ai]
                for disc in discs:
                    # Apaga todas as notas existentes para este aluno+disciplina
                    db.query(ModelNota).filter_by(
                        aluno_id=aluno.id,
                        disciplina_id=disc.id,
                    ).delete()
                    db.flush()

                    for bim in range(1, 5):
                        # Prova: maioria boa (6-10), alguns com dificuldade (3-6)
                        prova = round(random.choices(
                            [random.uniform(3, 5.9), random.uniform(6, 7.9), random.uniform(8, 10)],
                            weights=[0.18, 0.40, 0.42],
                        )[0], 1)

                        # Trabalho: ligeiramente melhor que prova
                        trabalho = round(min(10, prova + random.uniform(-0.5, 2.0)), 1)

                        db.add(ModelNota(
                            valor=prova,
                            tipo="prova",
                            bimestre=bim,
                            lancado_em=bimestre_dates[bim],
                            aluno_id=aluno.id,
                            disciplina_id=disc.id,
                        ))
                        db.add(ModelNota(
                            valor=trabalho,
                            tipo="trabalho",
                            bimestre=bim,
                            lancado_em=bimestre_dates[bim],
                            aluno_id=aluno.id,
                            disciplina_id=disc.id,
                        ))
                        notas_count += 2

                        # Recuperação: apenas se média prova+trabalho < 7
                        media_bim = (prova + trabalho) / 2
                        if media_bim < 7:
                            recuperacao = round(random.uniform(4.5, 8.5), 1)
                            db.add(ModelNota(
                                valor=recuperacao,
                                tipo="recuperacao",
                                bimestre=bim,
                                lancado_em=bimestre_dates[bim],
                                aluno_id=aluno.id,
                                disciplina_id=disc.id,
                            ))
                            notas_count += 1

        db.commit()
        print(f"  {notas_count} notas OK")

        # ── 9. FREQUÊNCIAS ────────────────────────────────────────────
        print("Inserindo frequências...")
        freq_count = 0
        # Simular 12 aulas por disciplina (3 por mês, 4 meses)
        aula_dates = [
            date(2025, 2, 10), date(2025, 2, 17), date(2025, 2, 24),
            date(2025, 3, 10), date(2025, 3, 17), date(2025, 3, 24),
            date(2025, 4,  7), date(2025, 4, 14), date(2025, 4, 22),
            date(2025, 5,  5), date(2025, 5, 12), date(2025, 5, 19),
        ]
        for turma_idx, aluno_idxs in turma_dist:
            turma = turmas[turma_idx]
            discs = disciplinas[turma.id][:4]  # apenas 4 disciplinas para não explodir
            for ai in aluno_idxs:
                aluno = alunos[ai]
                for disc in discs:
                    for dt in aula_dates:
                        existe = db.query(ModelFrequencia).filter_by(
                            aluno_id=aluno.id,
                            disciplina_id=disc.id,
                            data_aula=dt,
                        ).first()
                        if not existe:
                            presente = random.choices([True, False], weights=[0.88, 0.12])[0]
                            f = ModelFrequencia(
                                data_aula=dt,
                                presente=presente,
                                justificativa="Atestado médico" if not presente and random.random() > 0.5 else None,
                                disciplina_id=disc.id,
                                aluno_id=aluno.id,
                            )
                            db.add(f)
                            freq_count += 1
        db.commit()
        print(f"  {freq_count} frequências OK")

        # ── 10. MENSALIDADES & PAGAMENTOS ─────────────────────────────
        print("Inserindo mensalidades e pagamentos...")
        mens_count = 0
        pag_count = 0
        VALOR_MENSALIDADE = 650.00
        formas_pag = ["PIX", "Boleto", "Cartão de Débito", "Cartão de Crédito"]

        for aluno in alunos:
            for mes in range(2, 12):  # fev a nov/2025 (ano letivo completo)
                existe = db.query(ModelMensalidade).filter_by(
                    aluno_id=aluno.id, mes=mes, ano=2025
                ).first()
                if not existe:
                    vencimento = date(2025, mes, 10)
                    # Simula final de novembro: fev-set=pago, out=mix, nov=pendente/atrasado
                    if mes <= 9:
                        status = "pago"
                    elif mes == 10:
                        status = random.choices(["pago", "atrasado"], weights=[0.75, 0.25])[0]
                    else:  # nov
                        status = random.choices(["pago", "pendente", "atrasado"], weights=[0.35, 0.40, 0.25])[0]

                    m = ModelMensalidade(
                        aluno_id=aluno.id,
                        mes=mes,
                        ano=2025,
                        valor=VALOR_MENSALIDADE,
                        vencimento=vencimento,
                        status=status,
                    )
                    db.add(m)
                    db.flush()
                    mens_count += 1

                    # Criar pagamento se pago
                    if status == "pago":
                        p = ModelPagamento(
                            data_pagamento=date(2025, mes, random.randint(5, 10)),
                            valor_pago=VALOR_MENSALIDADE,
                            forma_pagamento=random.choice(formas_pag),
                            comprovante=None,
                            mensalidade_id=m.id,
                        )
                        db.add(p)
                        pag_count += 1
        db.commit()
        print(f"  {mens_count} mensalidades e {pag_count} pagamentos OK")

        # ── 11. COMUNICADOS ───────────────────────────────────────────
        print("Inserindo comunicados...")
        admin_user = usuarios["admin@escola.com"]
        comunicados_data = [
            (
                "Bem-vindos ao Ano Letivo 2025!",
                "Prezados alunos e responsáveis, é com grande satisfação que iniciamos mais um ano letivo. "
                "As aulas começam em 03 de fevereiro de 2025. Por favor, confiram o material necessário "
                "para cada disciplina na lista disponível na secretaria. Bom ano a todos!",
                date(2025, 1, 28),
                True,
            ),
            (
                "Calendário de Provas do 1º Bimestre",
                "Informamos que as provas do 1º Bimestre ocorrerão entre os dias 17 e 21 de março de 2025. "
                "Os alunos devem comparecer com 15 minutos de antecedência. Material permitido: caneta azul "
                "ou preta e régua. Calculadoras apenas para Matemática.",
                date(2025, 3, 5),
                True,
            ),
            (
                "Reunião de Pais e Mestres — 1º Bimestre",
                "Convidamos todos os responsáveis para a Reunião de Pais e Mestres referente ao 1º Bimestre. "
                "O evento ocorrerá no dia 05 de abril de 2025 (sábado), das 8h às 12h. "
                "A participação é muito importante para acompanhar o desenvolvimento do seu filho(a).",
                date(2025, 3, 25),
                True,
            ),
            (
                "Gincana Cultural 2025 — Inscrições Abertas",
                "Está aberto o período de inscrições para a Gincana Cultural 2025! As equipes devem ser "
                "formadas por turma, com no mínimo 5 e no máximo 10 alunos. A gincana acontecerá em "
                "23 de maio de 2025. Prêmios para as três melhores colocações. Inscrevam-se na secretaria!",
                date(2025, 4, 15),
                True,
            ),
            (
                "Aviso: Manutenção da Quadra Esportiva",
                "Informamos que a quadra esportiva estará em manutenção nos dias 28 e 29 de abril de 2025. "
                "As aulas de Educação Física serão realizadas no pátio coberto durante este período.",
                date(2025, 4, 22),
                True,
            ),
            (
                "Calendário de Provas do 2º Bimestre",
                "As provas do 2º Bimestre estão programadas para os dias 26 a 30 de maio de 2025. "
                "Lembramos que a revisão das matérias é de responsabilidade do aluno. "
                "Dúvidas podem ser esclarecidas com os professores nas aulas de apoio.",
                date(2025, 5, 12),
                True,
            ),
            (
                "Feira de Ciências 2025",
                "A Feira de Ciências deste ano terá como tema 'Sustentabilidade e Meio Ambiente'. "
                "Os projetos deverão ser apresentados em 20 de junho de 2025. Cada turma deve apresentar "
                "ao menos dois trabalhos. Maiores informações com a coordenação pedagógica.",
                date(2025, 5, 28),
                True,
            ),
            (
                "Recesso de Julho — Período de Férias",
                "Comunicamos que o recesso escolar do meio do ano ocorrerá de 14 a 25 de julho de 2025. "
                "As aulas retornam normalmente em 28 de julho. Aproveitem o período para descanso e "
                "revisão do conteúdo do 1º semestre.",
                date(2025, 6, 30),
                False,
            ),
        ]
        com_count = 0
        for titulo, conteudo, enviado_em, ativo in comunicados_data:
            existe = db.query(ModelComunicado).filter_by(titulo=titulo).first()
            if not existe:
                c = ModelComunicado(
                    titulo=titulo,
                    conteudo=conteudo,
                    destinatario_id=admin_user.id,
                    enviado_em=enviado_em,
                    ativo=ativo,
                )
                db.add(c)
                com_count += 1
        db.commit()
        print(f"  {com_count} comunicados OK")

        print("\nSeed concluido com sucesso!")
        print(f"  Perfis: {len(perfis)}")
        print(f"  Usuários: {len(usuarios)}")
        print(f"  Turmas: {len(turmas)}")
        print(f"  Alunos: {len(alunos)}")
        print(f"  Mensalidades: {mens_count} | Pagamentos: {pag_count}")
        print(f"  Comunicados: {com_count}")
        print("\nCredenciais de acesso:")
        print("  admin@escola.com     / admin123")
        print("  secretaria@escola.com / sec123")
        print("  coord@escola.com     / coord123")
        print("  financeiro@escola.com / fin123")

    except Exception as e:
        db.rollback()
        print(f"\nErro durante o seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
