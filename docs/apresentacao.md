# EduGestão — Apresentação TDE 2026.1

> UNIFAN · Métodos Ágeis · Prof. Júlio César Andrade
> Equipe: Kauan Brandão · Kevin Mascarenhas · João Lucca

---

## 1. CRUD e Integração com a Interface

O sistema implementa CRUD completo para todos os módulos, com dados persistidos no PostgreSQL (Supabase) e apresentados no frontend React em tempo real.

| Módulo | C | R | U | D |
|---|:---:|:---:|:---:|:---:|
| Alunos | ✓ | ✓ | ✓ | ✓ |
| Matrículas | ✓ | ✓ | ✓ | ✓ |
| Turmas & Disciplinas | ✓ | ✓ | ✓ | ✓ |
| Professores | ✓ | ✓ | ✓ | ✓ |
| Notas & Frequência | ✓ | ✓ | ✓ | ✓ |
| Financeiro (Mensalidades/Pagamentos) | ✓ | ✓ | ✓ | ✓ |
| Comunicados | ✓ | ✓ | ✓ | ✓ |
| Usuários | ✓ | ✓ | ✓ | ✓ |

**Destaques de negócio:**
- Matrícula gera automaticamente 12 mensalidades (vencimento dia 10 de cada mês)
- Dashboard com KPIs em tempo real: inadimplência, média geral, frequência por turma
- Boletim com notas por trimestre e busca de aluno por digitação

**Deploy em produção:** https://erp-escolar.vercel.app

---

## 2. Processo de Desenvolvimento Ágil

Utilizamos **GitHub Projects** + **Pull Requests** como ferramenta de gestão, com fluxo Kanban: `Backlog → Em andamento → Em revisão → Concluído`.

**Práticas adotadas:**
- Cada funcionalidade desenvolvida em branch separada (`feat/`, `fix/`, `docs/`)
- Nenhum commit direto na `main` — tudo via Pull Request com descrição do que foi feito
- Commits atômicos e descritivos seguindo Conventional Commits (`feat:`, `fix:`, `docs:`)
- Distribuição de tarefas entre os três integrantes ao longo das sprints

**Evidências:** histórico de PRs no repositório GitHub com +25 pull requests mergeados.

---

## 3. Arquitetura do Sistema

```
Requisição HTTP
      ↓
  Router (FastAPI)    — valida entrada via Pydantic
      ↓
  Service             — regras de negócio
      ↓
  Repository          — queries SQLAlchemy
      ↓
  PostgreSQL (Supabase)
```

**Camadas:**
- **`routers/`** — endpoints REST, autenticação JWT, controle de acesso RBAC
- **`services/`** — regras de negócio (ex: geração de mensalidades, validações)
- **`repositories/`** — queries isoladas, sem lógica de negócio
- **`models/`** — mapeamento ORM das tabelas
- **`schemas/`** — validação e serialização com Pydantic v2
- **`domain/`** — entidades OOP demonstrando herança e polimorfismo (`Administrador`, `Operador` herdam de `Usuario`)

**Frontend:** React 18 + Vite 5, organizado em `pages/`, `components/` e `api/` (cliente HTTP com JWT).

---

## 4. Controle de Versão

**Repositório:** https://github.com/KauanBrandao/erp-escolar

- README com stack, módulos, instruções de execução local e credenciais de teste
- Histórico consistente de commits com participação dos três integrantes
- Branches por funcionalidade, nunca commits diretos na `main`
- `.env` no `.gitignore` — credenciais nunca expostas no repositório

---

## 5. Modelagem Final do Banco de Dados

13 tabelas implementadas no PostgreSQL:

**Acadêmico:** `Alunos`, `Turmas`, `Disciplinas`, `Professores`, `Matriculas`, `Notas`, `Frequencias`

**Financeiro:** `Mensalidade`, `Pagamentos`

**Usuários/Acesso:** `Usuarios`, `Perfis`, `Responsaveis`, `Comunicados`

**Diagrama visual:** `docs/diagrama-banco.html` (ERD completo com todas as relações e colunas)

---

## 6. Domínio — Decisões Técnicas

**Autenticação e Segurança:**
- JWT com expiração + bcrypt para hash de senhas
- RBAC com 5 perfis: Administrador, Secretaria, Coordenação Pedagógica, Financeiro, Responsável
- Cada endpoint decorado com `require_permission()` — acesso negado retorna 403

**Persistência:**
- SQLAlchemy 2.0 com sessão por requisição (`get_db` via `Depends`)
- `create_all()` para criar tabelas; migrações manuais para alterações em produção
- Cascade delete tratado manualmente antes de remover registros pai (ex: nulificar `professor_id` nas disciplinas antes de deletar professor)

**Deploy:**
- Backend serverless na Vercel via `api/index.py` com handler ASGI
- Frontend buildado com Vite e servido como estático
- Banco no Supabase (PostgreSQL gerenciado)

**Stack resumida:**

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.12 + FastAPI |
| ORM | SQLAlchemy 2.0 |
| Validação | Pydantic v2 |
| Auth | JWT + bcrypt |
| Banco | PostgreSQL (Supabase) |
| Frontend | React 18 + Vite 5 |
| Deploy | Vercel |
