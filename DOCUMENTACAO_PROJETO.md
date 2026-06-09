# EduGestão — Documentação do Projeto

## O que é o projeto?

O **EduGestão** é um sistema ERP (Enterprise Resource Planning) voltado para gestão escolar. Ele centraliza em uma única plataforma web todas as operações administrativas e pedagógicas de uma escola: cadastro de alunos, turmas, disciplinas, notas, frequência, financeiro (mensalidades e pagamentos) e comunicados.

O sistema é acessado pelo navegador e possui controle de acesso por perfil — cada usuário vê e faz apenas o que seu cargo permite.

---

## Como o sistema funciona

### Fluxo geral

```
Usuário (navegador)
      ↓  requisição HTTP
  Frontend (React)
      ↓  chamada para /api/...
  Backend (FastAPI)
      ↓  consulta SQL
  Banco de Dados (PostgreSQL / Supabase)
```

1. O usuário acessa o site hospedado na **Vercel**
2. O frontend React carrega no navegador e exibe a tela de login
3. Ao fazer login, o backend valida as credenciais e devolve um **token JWT**
4. O token é salvo no navegador e enviado em todas as requisições seguintes
5. O backend verifica o token, identifica o perfil do usuário e decide se ele tem permissão para aquela ação
6. Os dados são buscados/salvos no banco **PostgreSQL** hospedado no **Supabase**

### Autenticação e permissões

O sistema usa **JWT (JSON Web Token)** para autenticação. Após o login, o token contém o ID do usuário e seu perfil. Cada rota da API verifica se o perfil tem a permissão necessária antes de responder.

Perfis disponíveis:

| Perfil | Permissões |
|---|---|
| Administrador | Acesso total |
| Secretaria | Alunos, responsáveis, turmas, matrículas |
| Coordenação Pedagógica | Disciplinas, notas, frequências, comunicados |
| Financeiro | Mensalidades e pagamentos |
| Responsável | Leitura: notas, frequências, mensalidades do filho |

---

## Arquitetura do Backend

O backend segue uma arquitetura em camadas, onde cada camada tem uma responsabilidade clara:

```
Router  →  Service  →  Repository  →  Banco de Dados
```

- **Router**: recebe a requisição HTTP, valida os dados de entrada (via Pydantic) e chama o Service
- **Service**: contém as regras de negócio (ex: "não pode matricular aluno em turma inativa")
- **Repository**: executa as queries no banco via SQLAlchemy
- **Model**: define a estrutura das tabelas do banco
- **Schema**: define o formato dos dados de entrada e saída da API

### Módulos do sistema

| Módulo | Descrição |
|---|---|
| Alunos | Cadastro completo de alunos com responsável vinculado |
| Responsáveis | Pais/responsáveis pelos alunos |
| Turmas | Agrupamento por série, turno e ano letivo |
| Disciplinas | Matérias vinculadas a cada turma |
| Matrículas | Vínculo entre aluno e turma (ativa/trancada/cancelada) |
| Notas | Lançamento por bimestre e tipo (prova/trabalho/recuperação) |
| Frequências | Registro de presença por aula e disciplina |
| Mensalidades | Geração das cobranças mensais por aluno |
| Pagamentos | Registro dos pagamentos de mensalidades |
| Comunicados | Avisos enviados pela escola |
| Usuários | Contas de acesso ao sistema |
| Perfis | Grupos de permissão |

---

## Stack de Tecnologias

### Backend

#### Python
Linguagem de programação principal do backend. Python é conhecida pela legibilidade e pela enorme quantidade de bibliotecas disponíveis. É amplamente usada em desenvolvimento web, ciência de dados e automação.

#### FastAPI
Framework web para construção de APIs em Python. É moderno, rápido e gera documentação automática (Swagger UI acessível em `/docs`). Usa tipagem do Python para validar dados automaticamente e suporta operações assíncronas.

#### SQLAlchemy
ORM (Object-Relational Mapper) — permite trabalhar com o banco de dados usando código Python em vez de SQL puro. Cada tabela do banco é representada como uma classe Python (Model). Suporta múltiplos bancos de dados (PostgreSQL, MySQL, SQLite, etc.).

#### Pydantic
Biblioteca de validação de dados. Define os schemas (formatos) que os dados de entrada e saída da API devem seguir. Integrada nativamente ao FastAPI — se os dados não estiverem no formato correto, a API rejeita automaticamente com uma mensagem de erro clara.

#### python-jose
Biblioteca para geração e verificação de tokens JWT (JSON Web Token). Usada para autenticação: após o login, gera um token assinado que o frontend envia em cada requisição para provar que o usuário está autenticado.

#### bcrypt / passlib
Bibliotecas para criptografia de senhas. As senhas nunca são salvas em texto puro no banco — são transformadas em um hash irreversível. Na hora do login, a senha digitada é comparada com o hash salvo.

#### python-dotenv
Carrega variáveis de ambiente do arquivo `.env` para o código. Usado para separar configurações sensíveis (como senha do banco) do código-fonte.

#### psycopg2
Driver de conexão entre Python e PostgreSQL. É o "tradutor" que permite o SQLAlchemy enviar comandos SQL para o banco PostgreSQL.

#### uvicorn
Servidor ASGI (Asynchronous Server Gateway Interface) — roda a aplicação FastAPI. É o processo que fica "escutando" as requisições HTTP e as repassa para o FastAPI.

---

### Frontend

#### React
Biblioteca JavaScript para construção de interfaces de usuário. Permite criar componentes reutilizáveis (botões, tabelas, modais) e atualizar a tela de forma eficiente sem recarregar a página inteira. Mantido pelo Meta (Facebook).

#### Vite
Ferramenta de build e desenvolvimento para projetos frontend modernos. Substitui o antigo Webpack com uma abordagem muito mais rápida. Em desenvolvimento, atualiza o navegador instantaneamente ao salvar um arquivo. Em produção, gera um bundle otimizado (arquivos JS/CSS comprimidos).

#### JavaScript (JSX)
O frontend é escrito em JavaScript com JSX — uma extensão de sintaxe que permite escrever HTML dentro do código JavaScript. O Vite converte o JSX em JavaScript puro que o navegador entende.

#### CSS Customizado
O sistema não usa nenhuma biblioteca de UI (como Bootstrap ou Tailwind). Todo o estilo foi escrito manualmente com CSS puro usando variáveis CSS (tokens de design) para manter consistência visual. O tema é azul escolar com fundo branco.

#### Fetch API
API nativa do navegador para fazer requisições HTTP. O arquivo `src/api/client.js` encapsula o Fetch com tratamento de erros, autenticação via token JWT e conversão automática de JSON.

---

### Banco de Dados

#### PostgreSQL
Sistema de gerenciamento de banco de dados relacional (SGBD) open-source. É um dos mais robustos e confiáveis do mercado, com suporte a transações, chaves estrangeiras, índices avançados e muito mais. Os dados do sistema (alunos, notas, pagamentos, etc.) são armazenados em tabelas relacionadas entre si.

#### Supabase
Plataforma que oferece PostgreSQL como serviço na nuvem (Database-as-a-Service). Além do banco em si, oferece painel visual para gerenciar os dados, backups automáticos, autenticação (não usada neste projeto) e uma API REST gerada automaticamente. Funciona como alternativa open-source ao Firebase.

---

### Infraestrutura e Deploy

#### Vercel
Plataforma de hospedagem focada em aplicações web. O projeto inteiro (frontend + backend) é hospedado na Vercel como uma **Serverless Function** — em vez de um servidor rodando 24h, o código é executado sob demanda a cada requisição. Isso reduz custo e elimina a necessidade de gerenciar servidores.

#### Git + GitHub
Git é o sistema de controle de versão — registra todo o histórico de alterações no código. GitHub é a plataforma que hospeda o repositório remotamente. A Vercel está conectada ao GitHub: a cada push no branch `main`, um novo deploy é feito automaticamente.

#### Variáveis de Ambiente
Configurações sensíveis (como a URL do banco com senha) são armazenadas como variáveis de ambiente na Vercel, nunca no código-fonte. O backend as lê em tempo de execução via `os.getenv()`.

---

## Estrutura de Pastas

```
erp-escolar/
├── api/
│   └── index.py          # Ponto de entrada para a Vercel (importa o FastAPI)
├── core/
│   ├── database.py       # Configuração do SQLAlchemy e conexão com o banco
│   ├── security.py       # Funções de hash de senha e geração de JWT
│   ├── auth_dependencies.py  # Dependência FastAPI para verificar token
│   └── rbac.py           # Mapeamento de perfis → permissões
├── models/               # Classes SQLAlchemy (uma por tabela do banco)
├── schemas/              # Classes Pydantic (validação de entrada/saída)
├── repositories/         # Queries no banco (CRUD)
├── services/             # Regras de negócio
├── routers/              # Rotas da API (endpoints HTTP)
├── domain/               # Classes de domínio OOP (conceitual/acadêmico)
├── frontend/
│   ├── src/
│   │   ├── api/client.js     # Cliente HTTP com autenticação
│   │   ├── components/       # Componentes reutilizáveis (Modal, Sidebar, Toast...)
│   │   ├── pages/            # Páginas da aplicação (Alunos, Turmas, Boletim...)
│   │   ├── App.jsx           # Roteamento entre páginas
│   │   ├── index.css         # Design system (variáveis, componentes CSS)
│   │   └── main.jsx          # Ponto de entrada do React
│   ├── dist/                 # Build de produção (gerado pelo Vite)
│   └── package.json          # Dependências Node.js
├── main.py               # Aplicação FastAPI principal
├── requirements.txt      # Dependências Python
├── vercel.json           # Configuração de deploy na Vercel
├── seed.py               # Script para popular o banco com dados iniciais
└── .env                  # Variáveis de ambiente locais (não versionado)
```

---

## Endpoints da API

A documentação interativa completa está disponível em `/docs` (Swagger UI gerado automaticamente pelo FastAPI).

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/auth/login` | Login, retorna token JWT |
| GET | `/api/alunos/` | Lista todos os alunos |
| POST | `/api/alunos/` | Cadastra novo aluno |
| GET | `/api/turmas/` | Lista turmas |
| GET | `/api/notas/` | Lista notas |
| GET | `/api/frequencias/` | Lista frequências |
| GET | `/api/mensalidades/` | Lista mensalidades |
| GET | `/api/comunicados/` | Lista comunicados |
| ... | ... | (e mais para cada módulo) |

---

## Como rodar localmente

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- PostgreSQL local ou conta no Supabase

### Backend

```bash
# Instalar dependências Python
pip install -r requirements.txt

# Configurar banco no .env
echo "DATABASE_URL=postgresql://usuario:senha@localhost:5432/erp_escolar" > .env

# Rodar o servidor
uvicorn main:app --reload --port 8000
```

### Frontend (desenvolvimento)

```bash
cd frontend

# Instalar dependências Node
npm install

# Configurar a URL do backend
echo "VITE_API_URL=http://localhost:8000" > .env.local

# Rodar o servidor de desenvolvimento
npm run dev
```

### Popular o banco com dados de exemplo

```bash
python seed.py
```

Credenciais criadas pelo seed:

| Email | Senha | Perfil |
|---|---|---|
| admin@escola.com | admin123 | Administrador |
| secretaria@escola.com | sec123 | Secretaria |
| coord@escola.com | coord123 | Coordenação Pedagógica |
| financeiro@escola.com | fin123 | Financeiro |

---

## Deploy (Vercel + Supabase)

1. Fazer push para o branch `main` no GitHub
2. A Vercel detecta o push e inicia um novo deploy automaticamente
3. O backend roda como Serverless Function (`api/index.py`)
4. O banco PostgreSQL fica no Supabase (região us-east-1)
5. A conexão usa o **Connection Pooler** do Supabase (porta 6543) para compatibilidade com a Vercel Free

---

*Projeto desenvolvido como sistema de gestão escolar com arquitetura em camadas, separação clara de responsabilidades e deploy serverless.*
