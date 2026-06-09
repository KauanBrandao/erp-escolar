# Modelagem Final do Banco de Dados — EduGestão

> TDE Métodos Ágeis 2026.1 · UNIFAN

---

## Tabelas

### Perfis
| Campo | Tipo | Restrição |
|---|---|---|
| id | INTEGER | PK |
| nome | VARCHAR | NOT NULL |
| descricao | VARCHAR | — |

---

### Usuarios
| Campo | Tipo | Restrição |
|---|---|---|
| id | INTEGER | PK |
| nome | VARCHAR | NOT NULL |
| email | VARCHAR | NOT NULL |
| senha_hash | VARCHAR | NOT NULL |
| ativo | BOOLEAN | DEFAULT true |
| criado_em | DATE | — |
| perfil_id | INTEGER | FK → Perfis.id |

---

### Responsaveis
| Campo | Tipo | Restrição |
|---|---|---|
| id | INTEGER | PK |
| nome | VARCHAR | NOT NULL |
| cpf | VARCHAR | — |
| telefone | VARCHAR | — |
| email | VARCHAR | — |
| parentesco | INTEGER | FK → Usuarios.id |

---

### Alunos
| Campo | Tipo | Restrição |
|---|---|---|
| id | INTEGER | PK |
| nome | VARCHAR | NOT NULL |
| cpf | VARCHAR | — |
| telefone | VARCHAR | — |
| matricula_numero | INTEGER | — |
| ativo | BOOLEAN | DEFAULT true |
| data_nascimento | DATE | — |
| criado_em | DATE | — |
| responsavel_id | INTEGER | FK → Responsaveis.id |

---

### Turmas
| Campo | Tipo | Restrição |
|---|---|---|
| id | INTEGER | PK |
| nome | VARCHAR | NOT NULL |
| serie | VARCHAR | — |
| turno | VARCHAR | — |
| ano_letivo | INTEGER | — |
| perfil_id | INTEGER | FK → Perfis.id |

---

### Professores
| Campo | Tipo | Restrição |
|---|---|---|
| id | INTEGER | PK |
| nome | VARCHAR | NOT NULL |
| cpf | VARCHAR | — |
| email | VARCHAR | — |
| telefone | VARCHAR | — |
| especialidade | VARCHAR | — |
| ativo | BOOLEAN | DEFAULT true |
| criado_em | DATE | — |

---

### Disciplinas
| Campo | Tipo | Restrição |
|---|---|---|
| id | INTEGER | PK |
| nome | VARCHAR | NOT NULL |
| codigo | VARCHAR | — |
| carga_horaria | INTEGER | — |
| turma_id | INTEGER | FK → Turmas.id |
| professor_id | INTEGER | FK → Professores.id (nullable) |

---

### Matriculas
| Campo | Tipo | Restrição |
|---|---|---|
| id | INTEGER | PK |
| aluno_id | INTEGER | FK → Alunos.id |
| turma_id | INTEGER | FK → Turmas.id |
| data_matricula | DATE | — |
| status | VARCHAR | — |
| observacao | TEXT | — |

---

### Notas
| Campo | Tipo | Restrição |
|---|---|---|
| id | INTEGER | PK |
| valor | DECIMAL | NOT NULL |
| tipo | VARCHAR | — |
| trimestre | INTEGER | — |
| lancado_em | DATE | — |
| aluno_id | INTEGER | FK → Alunos.id |
| disciplina_id | INTEGER | FK → Disciplinas.id |

---

### Frequencias
| Campo | Tipo | Restrição |
|---|---|---|
| id | INTEGER | PK |
| data_aula | DATE | NOT NULL |
| presente | BOOLEAN | — |
| justificativa | TEXT | — |
| disciplina_id | INTEGER | FK → Disciplinas.id |
| aluno_id | INTEGER | FK → Alunos.id |

---

### Mensalidade
| Campo | Tipo | Restrição |
|---|---|---|
| id | INTEGER | PK |
| aluno_id | INTEGER | FK → Alunos.id |
| mes | INTEGER | — |
| ano | INTEGER | — |
| valor | FLOAT | — |
| vencimento | DATE | — |
| status | VARCHAR | — |

---

### Pagamentos
| Campo | Tipo | Restrição |
|---|---|---|
| id | INTEGER | PK |
| data_pagamento | DATE | — |
| valor_pago | FLOAT | — |
| forma_pagamento | VARCHAR | — |
| comprovante | VARCHAR | — |
| mensalidade_id | INTEGER | FK → Mensalidade.id |

---

### Comunicados
| Campo | Tipo | Restrição |
|---|---|---|
| id | INTEGER | PK |
| titulo | VARCHAR | NOT NULL |
| conteudo | TEXT | — |
| destinatario_id | INTEGER | FK → Usuarios.id |
| enviado_em | DATE | — |
| ativo | BOOLEAN | DEFAULT true |

---

## Relacionamentos

```
Perfis ──────────────< Usuarios          (um perfil possui vários usuários)
Perfis ──────────────< Turmas            (um perfil vincula várias turmas)
Usuarios ────────────< Responsaveis      (usuário referenciado como parentesco)
Usuarios ────────────< Comunicados       (destinatário do comunicado)
Responsaveis ────────< Alunos            (um responsável por vários alunos)
Alunos ──────────────< Matriculas        (um aluno realiza várias matrículas)
Turmas ──────────────< Matriculas        (uma turma recebe várias matrículas)
Turmas ──────────────< Disciplinas       (uma turma contém várias disciplinas)
Professores ─────────< Disciplinas       (um professor leciona várias disciplinas)
Alunos ──────────────< Notas             (um aluno recebe várias notas)
Disciplinas ─────────< Notas             (uma disciplina gera várias notas)
Alunos ──────────────< Frequencias       (um aluno registra várias frequências)
Disciplinas ─────────< Frequencias       (uma disciplina registra várias frequências)
Alunos ──────────────< Mensalidade       (um aluno possui várias mensalidades)
Mensalidade ─────────< Pagamentos        (uma mensalidade é quitada por pagamentos)
```

---

## Resumo

| | Quantidade |
|---|---|
| Tabelas | 13 |
| Relacionamentos | 15 |
| Chaves estrangeiras | 16 |
