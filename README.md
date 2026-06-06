# ERP Escolar — Sistema de Gestão Educacional

Sistema completo de gestão escolar desenvolvido como Trabalho de Desenvolvimento de Software (TDE) — Programação Orientada a Objetos 2026.1.

## Tecnologias

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3 + FastAPI |
| ORM | SQLAlchemy 2.0 |
| Banco de dados | MySQL |
| Validação | Pydantic v2 |
| Servidor | Uvicorn |
| Frontend | React 18 + Vite 5 |

## Pré-requisitos

- Python 3.11+
- Node.js 18+
- MySQL 8.0+ rodando localmente

## Instalação e Execução

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd erp-escolar
```

### 2. Configure o banco de dados

Crie o banco no MySQL:

```sql
CREATE DATABASE erp_escolar;
```

Edite o arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=mysql+mysqlconnector://root:sua_senha@localhost:3306/erp_escolar
```

### 3. Backend (FastAPI)

```bash
# Instale as dependências
pip install -r requirements.txt

# Inicie o servidor (as tabelas são criadas automaticamente)
python -m uvicorn main:app --reload
```

O backend estará disponível em `http://localhost:8000`
Documentação automática da API: `http://localhost:8000/docs`

### 4. Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

O frontend estará disponível em `http://localhost:3000`

## Estrutura do Projeto

```
erp-escolar/
├── main.py                  # Ponto de entrada da aplicação
├── requirements.txt         # Dependências Python
├── .env                     # Variáveis de ambiente (não versionar)
│
├── models/                  # Modelos ORM (tabelas do banco)
├── schemas/                 # Schemas Pydantic (validação / DTOs)
├── repositories/            # Acesso ao banco de dados (queries)
├── services/                # Regras de negócio
├── routers/                 # Endpoints da API (controllers)
├── domain/                  # Entidades de domínio (OOP)
├── utils/                   # Utilitários (logger, etc.)
│
└── frontend/                # Interface React
    └── src/
        ├── api/             # Cliente HTTP centralizado
        ├── components/      # Componentes reutilizáveis
        └── pages/           # Telas do sistema
```

## Módulos do Sistema

| Módulo | Rota API | Funcionalidades |
|--------|----------|-----------------|
| Alunos | `/alunos` | Cadastro, consulta, edição e remoção de alunos |
| Matrículas | `/matriculas` | Vínculo aluno-turma com status (ativa/trancada/cancelada) |
| Turmas | `/turmas` | Gestão de turmas por série, turno e ano letivo |
| Disciplinas | `/disciplinas` | Disciplinas vinculadas às turmas |
| Notas | `/notas` | Lançamento de notas por bimestre e tipo (prova/trabalho/recuperação) |
| Frequência | `/frequencias` | Registro de presença por aula e disciplina |
| Mensalidades | `/mensalidades` | Geração de cobranças mensais por aluno |
| Pagamentos | `/pagamentos` | Registro de pagamentos com forma e comprovante |
| Comunicados | `/comunicados` | Avisos e comunicados para usuários do sistema |
| Usuários | `/usuarios` | Gerenciamento de acesso com perfis de permissão |
| Responsáveis | `/responsaveis` | Cadastro de responsáveis pelos alunos |
| Perfis | `/perfis` | Perfis de acesso (Administrador, Operador) |

## Arquitetura

O projeto adota a arquitetura em camadas **Controller → Service → Repository**:

```
Requisição HTTP
      ↓
  Router (Controller)   — recebe e valida a requisição, chama o Service
      ↓
  Service               — aplica regras de negócio
      ↓
  Repository            — executa queries no banco via SQLAlchemy
      ↓
  Banco de Dados (MySQL)
```

O módulo `domain/` implementa conceitos de **POO**: herança, polimorfismo e encapsulamento por meio das classes `Administrador` e `Operador` que herdam de `Usuario`.

## Rotas de Exemplo

```bash
# Listar todos os alunos
GET http://localhost:8000/alunos

# Cadastrar novo aluno
POST http://localhost:8000/alunos

# Buscar permissões de um usuário (polimorfismo)
GET http://localhost:8000/usuarios/{id}/permissoes

# Documentação interativa completa
GET http://localhost:8000/docs
```

## Contribuidores

Projeto desenvolvido em grupo — UNIFAN, 2026.1.
