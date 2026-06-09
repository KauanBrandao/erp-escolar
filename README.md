# EduGestão — Sistema de Gestão Escolar

> TDE — Métodos Ágeis 2026.1 | UNIFAN — Centro Universitário Nobre
> Prof. Júlio César Andrade

Sistema ERP web completo para gestão escolar, cobrindo módulos acadêmicos e financeiros com controle de acesso por perfil de usuário.

**Deploy em produção:** https://erp-escolar.vercel.app

---

## Equipe

- Kauan Brandão
- Kevin Mascarenhas
- João Lucca

---

## Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.12 + FastAPI |
| ORM | SQLAlchemy 2.0 |
| Validação | Pydantic v2 |
| Autenticação | JWT (python-jose) + bcrypt |
| Banco de Dados | PostgreSQL (Supabase) |
| Servidor | Uvicorn |
| Frontend | React 18 + Vite 5 |
| Deploy | Vercel (Serverless) |

---

## Módulos do Sistema

| Módulo | Descrição |
|---|---|
| Dashboard | Visão geral com KPIs em tempo real: alunos ativos, média geral, frequência, inadimplência, desempenho por turma e alunos em atenção |
| Alunos & Matrículas | Cadastro de alunos com geração automática de 12 mensalidades ao matricular (vencimento dia 10 de cada mês) |
| Turmas & Disciplinas | Gestão de turmas por série, turno e ano letivo; disciplinas com professor responsável vinculado |
| Professores | Cadastro completo de professores com especialidade, vínculo a disciplinas e controle de status |
| Boletim & Frequência | Notas por trimestre (1°/2°/3°) e tipo (prova/trabalho/recuperação); frequência por aula com resumo e busca por digitação |
| Financeiro | Mensalidades geradas automaticamente por matrícula; filtros por ano, mês e status; registro de pagamento com forma e comprovante |
| Comunicados | Avisos e comunicados institucionais |
| Usuários | Contas com perfis e permissões (RBAC) |

---

## Perfis de Acesso (RBAC)

| Perfil | Permissões |
|---|---|
| Administrador | Acesso total |
| Secretaria | Alunos, turmas, matrículas, professores (leitura e escrita) |
| Coordenação Pedagógica | Disciplinas, notas, frequências, comunicados, leitura de professores |
| Financeiro | Mensalidades e pagamentos |
| Responsável | Leitura: notas, frequências e mensalidades |

---

## Arquitetura

O projeto segue arquitetura em camadas com separação clara de responsabilidades:

```
Requisição HTTP
      ↓
  Router (FastAPI)       — valida entrada via Pydantic, chama Service
      ↓
  Service                — regras de negócio
      ↓
  Repository             — queries SQLAlchemy
      ↓
  PostgreSQL (Supabase)
```

O módulo `domain/` demonstra conceitos de **POO**: herança, polimorfismo e encapsulamento por meio das classes `Administrador` e `Operador` que herdam de `Usuario`.

---

## Como Executar Localmente

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- Conta no Supabase (ou PostgreSQL local)

### 1. Clone o repositório

```bash
git clone https://github.com/KauanBrandao/erp-escolar.git
cd erp-escolar
```

### 2. Configure o ambiente

```bash
# Crie o arquivo .env na raiz
DATABASE_URL=postgresql://postgres:SENHA@db.PROJETO.supabase.co:5432/postgres
```

### 3. Backend

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API disponível em `http://localhost:8000`
Documentação Swagger: `http://localhost:8000/docs`

### 4. Frontend

```bash
cd frontend
npm install

# Crie frontend/.env.local
echo "VITE_API_URL=http://localhost:8000" > .env.local

npm run dev
```

Frontend disponível em `http://localhost:3000`

### 5. Popular o banco com dados de exemplo

```bash
python seed.py
```

**Credenciais de acesso:**

| Email | Senha | Perfil |
|---|---|---|
| admin@escola.com | admin123 | Administrador |
| secretaria@escola.com | sec123 | Secretaria |
| coord@escola.com | coord123 | Coordenação |
| financeiro@escola.com | fin123 | Financeiro |

---

## Estrutura de Pastas

```
erp-escolar/
├── api/index.py          # Ponto de entrada Vercel
├── core/                 # Database, segurança, auth, RBAC
├── models/               # Modelos SQLAlchemy (tabelas)
├── schemas/              # Schemas Pydantic (validação)
├── repositories/         # Queries no banco
├── services/             # Regras de negócio
├── routers/              # Endpoints da API
├── domain/               # Entidades OOP (herança/polimorfismo)
├── frontend/
│   ├── src/
│   │   ├── api/          # Cliente HTTP com JWT
│   │   ├── components/   # Modal, Sidebar, Toast, StateBox
│   │   └── pages/        # Alunos, Turmas, Boletim, Financeiro...
│   └── dist/             # Build de produção
├── main.py               # App FastAPI
├── seed.py               # Script de dados iniciais
├── requirements.txt      # Dependências Python
└── vercel.json           # Config de deploy
```

---

## Dependências principais

```bash
pip install -r requirements.txt
```

| Pacote | Versão | Função |
|---|---|---|
| fastapi | 0.135.2 | Framework web |
| sqlalchemy | 2.0.48 | ORM |
| pydantic | 2.12.5 | Validação |
| psycopg2-binary | 2.9.10 | Driver PostgreSQL |
| python-jose | 3.5.0 | JWT |
| bcrypt | 4.3.0 | Hash de senhas |
| uvicorn | 0.42.0 | Servidor ASGI |
| python-dotenv | 1.2.2 | Variáveis de ambiente |
