# API de Gestão Escolar 📚

Uma API robusta para gerenciamento escolar, construída em Python. Este projeto utiliza uma arquitetura em camadas (Controller-Service-Repository) para garantir que o código seja escalável, fácil de manter e que cada componente tenha uma responsabilidade única.

## 🏗️ Arquitetura e Estrutura de Pastas

O projeto foi organizado separando as rotas da web, as regras de negócio e o acesso ao banco de dados. Abaixo está a explicação detalhada de cada diretório dentro de `app/`:

```text
app/
├── routers/          # Controladores (Endpoints)
├── services/         # Regras de Negócio
├── repositories/     # Consultas ao Banco de Dados (Queries)
├── models/           # Entidades do Banco (SQLAlchemy)
├── schemas/          # Validação de Dados (Pydantic / DTOs)
├── core/             # Configurações globais e Segurança (ou config/)
└── main.py           # Ponto de entrada da aplicação
```


### 📂 O que cada pasta faz?

* **`routers/` (Controladores):** É a porta de entrada da API. Aqui ficam os endpoints (`/alunos`, `/turmas`, etc.). Esta camada apenas recebe as requisições HTTP, repassa os dados para o `Service` adequado e devolve a resposta ao cliente.
* **`services/` (Regras de Negócio):** O cérebro da aplicação. Aqui ficam as validações lógicas e processos de negócio (ex: verificar se um aluno tem pendências antes de efetuar uma matrícula). Não possui conhecimento sobre rotas HTTP ou sintaxe de banco de dados.
* **`repositories/` (Acesso a Dados):** A única camada que se comunica diretamente com o banco de dados. Contém as operações de CRUD (Create, Read, Update, Delete) isolando as queries do resto do sistema.
* **`models/` (Entidades):** Classes que mapeiam as tabelas do banco de dados (geralmente usando o ORM SQLAlchemy). Cada classe representa uma tabela (ex: `AlunoModel` vira a tabela `alunos` no PostgreSQL).
* **`schemas/` (Contratos de API):** Classes de validação de dados (geralmente usando Pydantic). Funcionam como DTOs (*Data Transfer Objects*), garantindo que os JSONs de entrada e saída tenham o formato e os tipos corretos antes de chegarem aos controladores.
* **`core/` (ou `config/`):** O motor do sistema. Contém configurações de variáveis de ambiente (`.env`), setup de conexão com o banco de dados, middlewares, configurações de CORS e lógicas de segurança (como geração e validação de tokens JWT).
* **`main.py`:** O arquivo principal que inicializa a aplicação, registra todas as rotas e levanta o servidor web.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Framework Web:** FastAPI
* **Banco de Dados:** Mysql
* **ORM:** SQLAlchemy
* **Validação:** Pydantic
* **Ambiente:** Docker & Docker Compose
