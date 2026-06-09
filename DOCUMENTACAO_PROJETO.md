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

## Stack de Tecnologias — O que é cada coisa e por que usamos

---

### Backend (o "servidor" — código que roda na nuvem)

#### Python

**O que é:** Uma linguagem de programação. É o idioma em que o backend do sistema foi escrito.

**Por que usamos:** Python tem uma sintaxe simples e legível — o código se parece bastante com inglês estruturado. É uma das linguagens mais populares do mundo para desenvolvimento web, ciência de dados e automação. Tem uma biblioteca (pacote de código pronto) para praticamente qualquer necessidade.

**Analogia:** Se o sistema fosse uma receita, Python seria o português em que a receita está escrita.

---

#### FastAPI

**O que é:** Um framework web — uma estrutura que facilita a criação de APIs em Python.

**O que é uma API:** API (Application Programming Interface) é a "porta de comunicação" entre o frontend e o backend. Quando o sistema exibe a lista de alunos, o React (frontend) faz uma requisição para `/api/alunos` e o FastAPI responde com os dados em formato JSON. É uma conversa estruturada: o frontend pede, o backend responde.

**Por que usamos:** FastAPI é rápido, moderno e gera automaticamente uma documentação interativa acessível em `/docs` (Swagger UI) — você pode testar todos os endpoints diretamente no navegador sem escrever nenhum código extra.

**Analogia:** Se o sistema fosse um restaurante, a API seria o cardápio e o garçom. O cliente (frontend) pede um prato (dado), o garçom (FastAPI) leva o pedido para a cozinha (banco de dados) e traz o resultado.

---

#### SQLAlchemy

**O que é:** Um ORM — Object-Relational Mapper. Uma biblioteca que permite conversar com o banco de dados usando Python em vez de escrever SQL puro.

**Sem SQLAlchemy** você escreveria:
```sql
SELECT * FROM alunos WHERE ativo = true
```

**Com SQLAlchemy** você escreve:
```python
db.query(ModelAluno).filter_by(ativo=True).all()
```

O resultado é o mesmo, mas o código fica em Python e é mais seguro (evita SQL Injection automaticamente).

**Por que usamos:** Permite trocar de banco de dados (de PostgreSQL para MySQL, por exemplo) sem reescrever as queries. Cada tabela do banco vira uma classe Python (`ModelAluno`, `ModelTurma`, etc.) — fica mais fácil de entender e manter.

---

#### Pydantic

**O que é:** Uma biblioteca de validação de dados. Define exatamente qual formato os dados devem ter ao entrar e sair da API.

**Como funciona:** Você define um "schema" (molde) para cada tipo de dado:
```python
class AlunoCreate(BaseModel):
    nome: str        # obrigatório, texto
    cpf: str         # obrigatório, texto
    ativo: bool      # obrigatório, verdadeiro/falso
```

Se alguém mandar uma requisição sem o campo `nome`, ou mandar um número onde espera texto, o FastAPI rejeita automaticamente com uma mensagem de erro explicando o problema — sem você precisar escrever nenhuma verificação manual.

**Por que usamos:** Elimina uma classe inteira de bugs (dados no formato errado chegando ao banco). Integrado nativamente ao FastAPI.

---

#### JWT — JSON Web Token (python-jose)

**O que é:** Um sistema de autenticação baseado em tokens. Após o login, o servidor gera um "ticket" assinado digitalmente que o usuário carrega em todas as requisições seguintes.

**Como funciona na prática:**
1. Usuário envia email + senha para `/api/auth/login`
2. Backend verifica as credenciais e gera um token JWT
3. Token é salvo no `localStorage` do navegador
4. Cada requisição seguinte inclui o token no cabeçalho: `Authorization: Bearer TOKEN`
5. O backend verifica o token e identifica quem está fazendo o pedido

**Analogia:** É como uma pulseira de festival. Você prova sua identidade uma vez na entrada (login) e recebe a pulseira (token). A partir daí, qualquer área do evento reconhece a pulseira sem precisar ver seu documento novamente.

**Por que JWT e não sessão?** Sessões exigem que o servidor guarde estado (memória de quem está logado). JWT é "sem estado" (stateless) — o token contém todas as informações necessárias embutidas. Isso é essencial para Serverless Functions, onde cada requisição pode ser executada em uma instância diferente.

---

#### bcrypt (hash de senhas)

**O que é:** Uma função matemática de embaralhamento de senhas — irreversível por design.

**Por que não salvar a senha direto no banco?** Se o banco vazar, todas as senhas ficariam expostas. Com bcrypt, o que fica salvo é algo como `$2b$12$Xk8mP...` — um hash que não pode ser revertido para a senha original.

**Como funciona o login:**
1. Usuário digita `admin123`
2. Sistema aplica bcrypt na senha digitada
3. Compara o resultado com o hash salvo no banco
4. Se baterem, login autorizado

**Analogia:** É como uma impressão digital. Você não consegue reconstruir o dedo a partir da impressão, mas consegue comparar duas impressões para ver se são iguais.

---

#### psycopg2

**O que é:** O driver de conexão entre Python e PostgreSQL. Um "tradutor de protocolo" de baixo nível.

**Por que usamos:** PostgreSQL fala seu próprio protocolo de rede. O psycopg2 é a biblioteca que sabe esse protocolo e permite que o Python (via SQLAlchemy) se comunique com o banco. O desenvolvedor nunca chama o psycopg2 diretamente — o SQLAlchemy usa ele internamente.

**Analogia:** É como um cabo de rede. Você não interage com ele diretamente, mas sem ele nada funciona.

---

#### uvicorn

**O que é:** O servidor web que roda a aplicação FastAPI localmente.

**Por que precisamos?** O FastAPI é só o "código" — define as rotas e a lógica. Mas para que esse código fique "escutando" requisições HTTP, ele precisa de um servidor. O uvicorn faz esse papel.

**Uso:** Quando você roda `uvicorn main:app --reload`, o uvicorn inicia um processo que fica esperando conexões na porta 8000. O `--reload` faz ele reiniciar automaticamente ao detectar mudanças no código.

**Importante:** Na Vercel (produção), o uvicorn não é usado — a própria infraestrutura da Vercel gerencia a execução das Serverless Functions.

---

### Frontend (o que o usuário vê no navegador)

#### React

**O que é:** Uma biblioteca JavaScript para construir interfaces de usuário. Desenvolvida e mantida pelo Meta (Facebook).

**O problema que resolve:** Em HTML puro, atualizar a tela significa recarregar a página inteira. O React permite atualizar apenas a parte da tela que mudou, sem reload. Isso torna a experiência muito mais fluida — como um app de celular, não como um site dos anos 90.

**Conceito central — Componente:** No React, a interface é dividida em blocos reutilizáveis chamados componentes. O `Sidebar`, o `Modal`, os cards do `Dashboard` — cada um é um componente que pode ser usado em múltiplos lugares. Alterar o componente `Modal` atualiza todos os modais do sistema de uma vez.

**Analogia:** Pense em LEGO. Cada peça (componente) tem uma forma e função específica. Você monta a interface encaixando peças. Se quiser mudar o formato de um tipo de peça, todas as que usam aquele molde mudam automaticamente.

---

#### Vite

**O que é:** Uma ferramenta que transforma o código React (que o navegador não entende diretamente) em arquivos que o navegador entende.

**O problema:** O navegador só entende HTML, CSS e JavaScript puro. Mas o código React usa JSX (HTML misturado com JavaScript), importações de módulos (`import X from './X'`), variáveis de ambiente (`import.meta.env.VITE_API_URL`), e outras sintaxes modernas que o navegador não consegue executar diretamente.

**O que o Vite faz em dois modos:**

| Modo | Comando | O que faz |
|---|---|---|
| Desenvolvimento | `npm run dev` | Inicia um servidor local em `localhost:3000`. Ao salvar qualquer arquivo, o navegador atualiza instantaneamente (Hot Module Replacement) |
| Produção | `npm run build` | Converte todo o código em arquivos otimizados dentro de `frontend/dist/`. Esses arquivos são os que vão para o servidor |

**O que está em `frontend/dist/`** após o build:
- `index.html` — o HTML da aplicação
- `assets/index-HASH.js` — todo o JavaScript comprimido e otimizado
- `assets/index-HASH.css` — todo o CSS comprimido

**Analogia:** Vite é como um compilador de linguagem. Você escreve em "React" (JSX), o Vite "traduz" para JavaScript puro que o navegador entende. No modo de desenvolvimento ele faz essa tradução ao vivo, na hora. No modo de produção ele faz uma tradução otimizada de uma vez só e salva o resultado.

---

#### JSX

**O que é:** Uma extensão de sintaxe do JavaScript que permite escrever HTML dentro do código JavaScript.

**Sem JSX** (JavaScript puro):
```javascript
const elemento = React.createElement('div', { className: 'card' },
  React.createElement('h1', null, 'Olá, mundo')
)
```

**Com JSX** (muito mais legível):
```jsx
const elemento = (
  <div className="card">
    <h1>Olá, mundo</h1>
  </div>
)
```

O JSX não é HTML de verdade — é JavaScript disfarçado de HTML. O Vite converte o JSX para a forma sem JSX durante o build. Os arquivos `.jsx` são arquivos JavaScript com essa sintaxe especial.

---

#### CSS Customizado

**O que é:** O conjunto de estilos visuais do sistema, escrito manualmente em CSS puro.

**Por que não usamos Bootstrap ou Tailwind?** Bootstrap e Tailwind são bibliotecas de CSS prontas. Usá-las seria mais rápido para prototipagem, mas o resultado tende a ser genérico. O CSS customizado do EduGestão usa **variáveis CSS** (tokens de design) que centralizam as decisões visuais:

```css
:root {
  --primary: #1d6fbd;       /* cor azul do sistema */
  --sidebar-bg: #0d3b6e;    /* azul escuro da sidebar */
  --danger: #dc2626;        /* vermelho de erro */
}
```

Qualquer componente usa `color: var(--primary)` — se o azul mudar, muda em todo o sistema de uma vez só.

---

#### Fetch API

**O que é:** Uma função nativa do navegador para fazer requisições HTTP — é a forma que o React usa para "conversar" com o backend.

**Como usamos:** O arquivo `src/api/client.js` envolve o Fetch com funcionalidades extras: adiciona automaticamente o token JWT no cabeçalho de cada requisição, converte a resposta de JSON para objeto JavaScript, e redireciona para o login se o token expirar.

**Fluxo completo de uma requisição:**
```
React chama api.get('/alunos')
    → client.js adiciona o token JWT
    → navegador envia GET para /api/alunos
    → FastAPI verifica o token
    → SQLAlchemy busca no PostgreSQL
    → FastAPI retorna JSON
    → client.js converte para objeto JavaScript
    → React exibe os dados na tela
```

---

### Banco de Dados

#### PostgreSQL

**O que é:** Um sistema de banco de dados relacional — onde todos os dados do sistema são armazenados de forma permanente e organizada.

**Relacional** significa que os dados são organizados em **tabelas** (como planilhas Excel) com **relacionamentos** entre elas. Por exemplo:

- A tabela `alunos` tem uma coluna `responsavel_id`
- Essa coluna aponta para um registro na tabela `responsaveis`
- Assim o banco sabe qual responsável pertence a qual aluno sem duplicar dados

**Por que PostgreSQL e não MySQL, SQLite, etc.?** PostgreSQL é open-source, robusto, amplamente usado em produção no mundo real, e tem suporte excelente no Supabase. O SQLite seria mais simples mas não é adequado para múltiplos usuários simultâneos.

---

#### Supabase

**O que é:** Uma plataforma que oferece PostgreSQL como serviço na nuvem. Em vez de instalar e gerenciar um servidor de banco de dados você mesmo, o Supabase faz isso por você.

**O que o Supabase fornece neste projeto:**
- Um banco PostgreSQL acessível pela internet 24h
- Painel visual para ver e editar os dados (como um phpMyAdmin moderno)
- Backups automáticos
- **Connection Pooler** — um intermediário que gerencia as conexões com o banco de forma eficiente (necessário para compatibilidade com a Vercel)

**Por que não hospedar o banco na própria Vercel?** A Vercel é uma plataforma de hospedagem de código, não de banco de dados. Serverless Functions não podem manter um banco de dados internamente.

---

### Infraestrutura e Deploy

#### Vercel

**O que é:** A plataforma onde o sistema está hospedado — o que torna ele acessível pela internet.

**Modelo Serverless:** Em vez de um servidor dedicado rodando 24 horas, a Vercel executa o código apenas quando há uma requisição. Quando ninguém acessa, não existe nenhum processo rodando. Isso elimina custo e manutenção de servidor.

**Por que isso funciona para este projeto:** O uso é esporádico (não há requisições constantes), o que torna o modelo serverless ideal. O plano gratuito da Vercel suporta este tipo de aplicação sem custo.

---

#### Git + GitHub

**O que é:** Git é o sistema que registra todo o histórico de alterações no código. GitHub é o site que guarda esse histórico na nuvem.

**Por que isso importa para o deploy:** A Vercel está conectada ao repositório GitHub. Toda vez que um `git push` é feito no branch `main`, a Vercel detecta automaticamente e faz um novo deploy. Não existe nenhum passo manual de "publicar" — o ato de salvar o código no GitHub já dispara a publicação.

**Fluxo completo:**
```
Alterar código → git add → git commit → git push → GitHub → Vercel → Produção
```

---

#### Variáveis de Ambiente

**O que são:** Configurações que o sistema precisa para funcionar mas que não devem aparecer no código-fonte (especialmente no GitHub, que é público).

**Exemplo do problema:** A URL do banco de dados contém a senha:
```
postgresql://postgres.PROJETO:MINHA_SENHA@pooler.supabase.com:6543/postgres
```

Se isso fosse salvo no código e commitado no GitHub, qualquer pessoa poderia ver a senha e acessar o banco.

**Solução:** A senha fica armazenada no painel da Vercel (Settings → Environment Variables) e o código lê ela em tempo de execução:
```python
DATABASE_URL = os.getenv("DATABASE_URL")  # nunca está no código
```

Localmente, o arquivo `.env` cumpre esse papel — e ele está no `.gitignore`, então nunca vai para o GitHub.

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

## Deploy Automático — Como Funciona

### Visão geral do fluxo

```
Desenvolvedor
     │
     │  git push origin main
     ▼
  GitHub
     │
     │  webhook automático
     ▼
  Vercel
     │
     │  detecta push → inicia build → deploy
     ▼
  Produção (URL pública atualizada em ~30 segundos)
```

Não existe nenhuma etapa manual. Basta fazer `git push` e o sistema atualiza sozinho.

---

### O que a Vercel faz ao receber o push

1. **Clona o repositório** na versão do commit mais recente
2. **Detecta `api/index.py`** — qualquer arquivo Python dentro da pasta `api/` é tratado automaticamente como uma **Serverless Function**
3. **Instala as dependências** listadas em `requirements.txt`
4. **Coloca a função em produção** — a URL pública passa a apontar para este novo código

O build do frontend **não é executado pela Vercel** — os arquivos já compilados em `frontend/dist/` são commitados no repositório e servidos diretamente pelo FastAPI.

---

### O papel de cada arquivo de configuração

#### `vercel.json`

```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/api/index.py" }
  ]
}
```

Esta única regra diz à Vercel: **toda requisição HTTP** que chegar ao servidor (seja `GET /`, `GET /alunos`, `POST /api/auth/login`) deve ser encaminhada para `api/index.py`. Sem isso, a Vercel não saberia para onde rotear as requisições.

#### `api/index.py`

```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
```

É o **ponto de entrada da Serverless Function**. Ele apenas importa o objeto `app` do FastAPI definido em `main.py`. A Vercel exige que o arquivo esteja dentro de `api/` e que exporte um objeto compatível com ASGI (o FastAPI é ASGI por padrão).

#### `main.py` — roteamento unificado (backend + frontend)

O FastAPI cuida de duas responsabilidades:

| Rota | O que acontece |
|---|---|
| `/api/*` | Processado pelo FastAPI (autenticação, banco de dados, etc.) |
| `/assets/*` | Serve os arquivos JS/CSS do build do React |
| `/*` (qualquer outra) | Serve o `frontend/dist/index.html` — o React assume o controle no navegador |

Isso significa que **não existe um servidor separado para o frontend**. O próprio FastAPI serve os arquivos estáticos do React quando o caminho não começa com `/api/`.

---

### O que é uma Serverless Function

Em um servidor tradicional, o código fica rodando 24 horas por dia esperando requisições. Na Vercel (modelo serverless):

- A função **só existe durante a execução de uma requisição**
- Quando não há requisições, **não há processo rodando** (e portanto não há custo)
- Cada requisição pode ser executada em instâncias diferentes e paralelas
- O **primeiro acesso após um período inativo** pode ser um pouco mais lento (cold start — a função precisa inicializar)

Para este projeto, isso é ideal: o uso é esporádico e o custo é zero no plano gratuito.

---

### Variáveis de ambiente

O banco de dados não pode ter sua URL com senha exposta no código-fonte. Por isso ela é configurada diretamente no painel da Vercel e **nunca aparece no GitHub**.

**Como configurar:**

1. Acesse **vercel.com** → seu projeto → **Settings** → **Environment Variables**
2. Adicione:

| Nome | Valor | Ambiente |
|---|---|---|
| `DATABASE_URL` | `postgresql://postgres.SEU_ID:SENHA@aws-1-us-east-1.pooler.supabase.com:6543/postgres` | Production, Preview, Development |

3. Clique em **Save**
4. Faça um novo deploy (ou redeploy) para que a variável entre em vigor

O código lê essa variável em tempo de execução:

```python
# core/database.py
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
```

---

### Por que usar o Pooler do Supabase e não a conexão direta?

O Supabase oferece duas formas de conexão:

| Tipo | Porta | Protocolo |
|---|---|---|
| Conexão direta | 5432 | IPv6 |
| Connection Pooler (PgBouncer) | 6543 | IPv4 |

A Vercel Free **não suporta conexões IPv6 de saída**. Por isso, usar a URL da conexão direta (`db.SEU_ID.supabase.co:5432`) resulta em erro de rede. O Connection Pooler usa IPv4 e é compatível com a Vercel Free.

A URL correta tem o formato:

```
postgresql://postgres.SEU_PROJECT_ID:SENHA@aws-1-us-east-1.pooler.supabase.com:6543/postgres
```

---

### Resumo — o que precisa estar configurado para o deploy funcionar

| Item | Onde configurar | Feito uma vez? |
|---|---|---|
| Repositório GitHub conectado à Vercel | Vercel Dashboard → Import Project | Sim |
| `DATABASE_URL` com URL do pooler Supabase | Vercel → Settings → Environment Variables | Sim |
| `vercel.json` com a regra de rewrite | Arquivo no repositório | Sim |
| `api/index.py` importando o FastAPI | Arquivo no repositório | Sim |
| `frontend/dist/` com o build do React | Gerado com `npm run build` e commitado | A cada mudança no frontend |

---

*Projeto desenvolvido como sistema de gestão escolar com arquitetura em camadas, separação clara de responsabilidades e deploy serverless.*
