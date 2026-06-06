# Documentação Técnica — ERP Escolar

**Disciplina:** Programação Orientada a Objetos
**Instituição:** UNIFAN
**Período:** 2026.1

---

## 1. Visão Geral do Sistema

O **ERP Escolar** é um sistema web de gestão educacional que cobre o ciclo completo de uma escola: desde o cadastro de alunos e matrículas até o controle financeiro de mensalidades. O sistema é composto por uma API REST desenvolvida em **FastAPI (Python)** e uma interface web em **React**.

### Problema Resolvido

Escolas de pequeno e médio porte frequentemente gerenciam seus dados em planilhas ou sistemas fragmentados. O ERP Escolar centraliza em uma única plataforma:

- Gestão de alunos, responsáveis e matrículas
- Controle acadêmico (notas e frequência)
- Gestão financeira (mensalidades e pagamentos)
- Comunicação interna (comunicados)
- Controle de acesso por perfil de usuário

---

## 2. Arquitetura do Sistema

### 2.1 Visão em Camadas

```
┌─────────────────────────────────────────┐
│            FRONTEND (React)             │
│   Vite · CSS Custom · Fetch API         │
└──────────────────┬──────────────────────┘
                   │ HTTP / JSON
┌──────────────────▼──────────────────────┐
│           BACKEND (FastAPI)             │
│                                         │
│  ┌──────────┐  ┌──────────┐            │
│  │  Routers │→ │ Services │            │
│  │(Controllers)│ │(Regras de│            │
│  └──────────┘  │ Negócio) │            │
│                └──────┬───┘            │
│                       ↓               │
│              ┌──────────────┐          │
│              │ Repositories │          │
│              │(Acesso a dados)│         │
│              └──────┬───────┘          │
└─────────────────────┼───────────────────┘
                      │ SQLAlchemy ORM
┌─────────────────────▼───────────────────┐
│           BANCO DE DADOS (MySQL)        │
└─────────────────────────────────────────┘
```

### 2.2 Descrição das Camadas

| Camada | Responsabilidade | Tecnologia |
|--------|-----------------|------------|
| **Routers** | Receber requisições HTTP, validar entrada, retornar resposta | FastAPI + Pydantic |
| **Services** | Aplicar regras de negócio, orquestrar operações | Python puro |
| **Repositories** | Executar queries no banco de dados | SQLAlchemy 2.0 |
| **Models** | Mapear tabelas do banco como classes Python | SQLAlchemy ORM |
| **Schemas** | Definir contratos de entrada e saída da API (DTOs) | Pydantic v2 |
| **Domain** | Entidades de domínio com comportamento (POO) | Python puro |
| **Frontend** | Interface gráfica para interação do usuário | React + Vite |

### 2.3 Fluxo de uma Requisição

```
Usuário clica em "Novo Aluno"
        ↓
Frontend faz POST /alunos com JSON
        ↓
Router recebe, valida com Pydantic (AlunoCreate)
        ↓
ServiceAluno verifica regras de negócio
        ↓
AlunoRepository executa INSERT no MySQL
        ↓
Resposta JSON volta ao frontend
        ↓
Toast de sucesso exibido para o usuário
```

---

## 3. Modelagem do Banco de Dados

### 3.1 Diagrama de Entidades

```
PERFIS ──────────────── USUARIOS
  │                         │
  │                    COMUNICADOS
  │
RESPONSAVEIS
  │
ALUNOS ──────────────── MATRICULAS ─── TURMAS ─── DISCIPLINAS
  │                                                    │
  ├── NOTAS ──────────────────────────────────────────┘
  │
  ├── FREQUENCIAS ─────────────────────────────────────┘
  │
  └── MENSALIDADES ─── PAGAMENTOS
```

### 3.2 Descrição das Tabelas

| Tabela | Campos principais | Relacionamentos |
|--------|-------------------|-----------------|
| `alunos` | id, nome, cpf, telefone, matricula_numero, data_nascimento, ativo | → responsaveis |
| `responsaveis` | id, nome, cpf, telefone, email, parentesco | — |
| `turmas` | id, nome, serie, turno, ano_letivo | — |
| `disciplinas` | id, nome, codigo, carga_horaria | → turmas |
| `matriculas` | id, data_matricula, status, observacao | → alunos, turmas |
| `notas` | id, valor (0-10), tipo, bimestre, lancado_em | → alunos, disciplinas |
| `frequencias` | id, data_aula, presente, justificativa | → alunos, disciplinas |
| `mensalidades` | id, mes, ano, valor, vencimento, status | → alunos |
| `pagamentos` | id, data_pagamento, valor_pago, forma_pagamento, comprovante | → mensalidades |
| `usuarios` | id, nome, email, senha_hash, ativo, criado_em | → perfis |
| `perfis` | id, nome, descricao | — |
| `comunicados` | id, titulo, conteudo, ativo, enviado_em | → usuarios |

### 3.3 Criação Automática das Tabelas

As tabelas são criadas automaticamente ao iniciar o sistema via:

```python
Base.metadata.create_all(bind=engine)  # main.py
```

Não é necessário rodar migrations manualmente.

---

## 4. Orientação a Objetos no Projeto

O projeto demonstra os 4 pilares da POO:

### 4.1 Encapsulamento

Cada camada encapsula sua responsabilidade. O `Service` não conhece detalhes de SQL; o `Repository` não conhece regras de negócio.

```python
class ServiceMatricula:
    def criar(self, dados: MatriculaCreate):
        # Regra de negócio encapsulada aqui
        aluno = self.repo_aluno.buscar_por_id(dados.aluno_id)
        if not aluno:
            raise HTTPException(404, "Aluno não encontrado")
        return self.repo.criar(dados)
```

### 4.2 Herança

O módulo `domain/EntidadeBase.py` define uma classe abstrata base que é herdada por `AlunoEntidade` e `TurmaEntidade`:

```python
class EntidadeBase(ABC):
    @abstractmethod
    def validar(self): ...

    @abstractmethod
    def resumo(self): ...

class AlunoEntidade(EntidadeBase):
    def validar(self): ...   # implementação específica
    def resumo(self): ...    # implementação específica
```

### 4.3 Polimorfismo

O módulo `domain/UsuarioDominio.py` implementa polimorfismo: a função `get_permissoes()` retorna resultados diferentes dependendo do perfil do usuário.

```python
class Usuario(ABC):
    @abstractmethod
    def get_permissoes(self): ...

class Administrador(Usuario):
    def get_permissoes(self):
        return ["criar", "ler", "atualizar", "deletar", "gerenciar_usuarios"]

class Operador(Usuario):
    def get_permissoes(self):
        return ["criar", "ler", "atualizar"]
```

Acessível via endpoint: `GET /usuarios/{id}/permissoes`

### 4.4 Abstração

Os `Schemas` Pydantic abstraem a estrutura do banco, expondo apenas os campos necessários para a API:

```python
class AlunoResponse(AlunoBase):
    id: int
    criado_em: date
    # senha_hash, campos internos → nunca expostos
```

---

## 5. API REST — Endpoints

Todos os módulos seguem o padrão RESTful:

| Método | Rota | Ação |
|--------|------|------|
| GET | `/alunos` | Listar todos |
| POST | `/alunos` | Criar novo |
| GET | `/alunos/{id}` | Buscar por ID |
| PUT | `/alunos/{id}` | Atualizar |
| DELETE | `/alunos/{id}` | Remover |

O mesmo padrão se repete para: `/turmas`, `/disciplinas`, `/matriculas`, `/notas`, `/frequencias`, `/mensalidades`, `/pagamentos`, `/comunicados`, `/usuarios`, `/responsaveis`, `/perfis`.

**Rota especial (polimorfismo):**
```
GET /usuarios/{id}/permissoes
→ Retorna permissões dinâmicas baseadas no perfil do usuário
```

Documentação interativa completa disponível em: `http://localhost:8000/docs`

---

## 6. Frontend — Interface React

### 6.1 Telas Implementadas

| Tela | Funcionalidades |
|------|-----------------|
| **Alunos & Matrículas** | Lista, busca, filtro por status; CRUD completo de alunos; modal de matrícula com seleção de turma |
| **Turmas & Disciplinas** | Grid de turmas; painel lateral com disciplinas; CRUD de ambos |
| **Boletim & Frequência** | Seletor de aluno; tabela de notas por bimestre (prova/trabalho/recuperação); aba de frequência detalhada; lançamento de notas e frequências |
| **Financeiro** | Resumo (total, recebido, inadimplência); tabela de mensalidades; registro de pagamento com forma e comprovante |
| **Comunicados** | Cards com status ativo/inativo; CRUD completo; filtro por status |
| **Usuários** | Tabela com perfil de acesso; CRUD; avatar com iniciais |

### 6.2 Componentes Reutilizáveis

- **Modal + ConfirmDialog** — formulários e confirmação de exclusão
- **Toast** — notificações de sucesso/erro/aviso
- **Badge** — indicadores de status coloridos
- **Loading/Empty/ErrorBox** — estados de carregamento, vazio e erro

### 6.3 Comunicação com a API

Centralizada em `frontend/src/api/client.js`:

```javascript
const api = {
  get:  (path)       => request('GET',    path),
  post: (path, body) => request('POST',   path, body),
  put:  (path, body) => request('PUT',    path, body),
  del:  (path)       => request('DELETE', path),
}
```

---

## 7. Como Executar o Projeto

### Requisitos

- Python 3.11+
- Node.js 18+
- MySQL 8.0 rodando localmente

### Passo a Passo

```bash
# 1. Configure o banco
# Crie o banco 'erp_escolar' no MySQL
# Edite o .env com suas credenciais

# 2. Inicie o backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
# → http://localhost:8000
# → http://localhost:8000/docs  (documentação)

# 3. Inicie o frontend
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

---

## 8. Decisões Técnicas

| Decisão | Justificativa |
|---------|---------------|
| FastAPI em vez de Flask/Django | Suporte nativo a async, validação automática com Pydantic, geração automática de documentação (Swagger) |
| SQLAlchemy ORM | Abstração do banco de dados, facilitando troca de SGBD; migrações; relacionamentos declarativos |
| Pydantic v2 | Validação de dados robusta com tipagem, serialização automática, mensagens de erro claras |
| React + Vite | Build rápido, ecossistema moderno, componentes reutilizáveis, sem dependência de biblioteca de UI |
| CORS aberto em desenvolvimento | Permite que o frontend (porta 3000) se comunique com a API (porta 8000) sem bloqueio |
| Criação automática de tabelas | Elimina necessidade de rodar migrations manualmente em ambiente de desenvolvimento |

---

## 9. Estrutura de Arquivos Completa

```
erp-escolar/
├── main.py                        # App FastAPI, CORS, routers
├── requirements.txt
├── .env                           # DATABASE_URL
│
├── models/
│   ├── database.py                # Conexão SQLAlchemy
│   ├── ModelAluno.py
│   ├── ModelTurma.py
│   ├── ModelMatricula.py
│   ├── ModelDisciplina.py
│   ├── ModelNota.py
│   ├── ModelFrequencia.py
│   ├── ModelMensalidade.py
│   ├── ModelPagamento.py
│   ├── ModelComunicado.py
│   ├── ModelUsuario.py
│   ├── ModelResponsavel.py
│   └── ModelPerfil.py
│
├── schemas/                       # DTOs Pydantic (Create/Response/Update)
├── repositories/                  # CRUD isolado por entidade
├── services/                      # Regras de negócio
├── routers/                       # Endpoints REST
│
├── domain/
│   ├── EntidadeBase.py            # Classe abstrata (herança)
│   └── UsuarioDominio.py          # Polimorfismo de permissões
│
├── utils/
│   └── logger.py                  # Log de ações do sistema
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.jsx                # Roteamento por estado
        ├── index.css              # Design system
        ├── api/client.js          # Cliente HTTP
        ├── components/
        │   ├── Sidebar.jsx
        │   ├── Topbar.jsx
        │   ├── Modal.jsx
        │   ├── Toast.jsx
        │   └── StateBox.jsx
        └── pages/
            ├── Alunos.jsx
            ├── Turmas.jsx
            ├── Boletim.jsx
            ├── Financeiro.jsx
            ├── Comunicados.jsx
            └── Usuarios.jsx
```
