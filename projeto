# RoadMap DevOps — Do Zero ao CI/CD

> **Não conhece algum termo?** Leia primeiro o [`Conceitos.md`](Conceitos.md) — explica Python, Docker, Git, API, CRUD e tudo mais de forma objetiva para iniciantes.

> **Objetivo:** Treinar um DevOps iniciante a criar uma **API de usuários** (backend, sem front-end), containerizar com Docker, publicar no GitHub e validar tudo com GitHub Actions.
>
> **Tempo estimado:** 1 a 2 dias (dependendo da experiência prévia)
>
> **Pré-requisitos:** Linux ou Mac, acesso à internet, conta no GitHub

---

## Ferramentas que precisam estar instaladas na máquina

Antes de começar a Milestone 1, instale e confira tudo abaixo. Sem essas ferramentas, os passos seguintes não funcionam.

| Ferramenta | Para que serve | Obrigatória? |
|------------|----------------|--------------|
| **Git** | Versionar código e enviar para o GitHub | ✅ Sim |
| **Docker** | Criar e rodar containers (app + banco) | ✅ Sim |
| **Docker Compose** | Subir app e banco juntos com um comando | ✅ Sim |
| **curl** | Testar a API e rodar o script de validação | ✅ Sim |
| **Python 3** | Ler o JSON no script `validate.sh` | ✅ Sim |
| **Editor de código** (VS Code, Cursor, etc.) | Editar arquivos do projeto | ✅ Sim |
| **Navegador** | Acessar GitHub e ver a pipeline rodando | ✅ Sim |
| **Conta no GitHub** | Hospedar o repositório e rodar Actions | ✅ Sim |

> **GitHub Actions** roda na nuvem do GitHub — **não precisa instalar** na máquina local.

### Checklist antes de iniciar

- [ ] Git instalado
- [ ] Docker instalado e rodando (`docker run hello-world` funciona)
- [ ] Docker Compose instalado (`docker compose version` funciona)
- [ ] curl instalado
- [ ] Python 3 instalado
- [ ] Editor de código aberto e pronto
- [ ] Conta criada em [github.com](https://github.com)

---

## Visão geral das Milestones

| # | Milestone | O que você vai saber fazer ao final |
|---|-----------|-------------------------------------|
| 1 | App de usuários + Docker | Criar API de cadastro/login, banco de dados e rodar tudo com `docker compose up` |
| 2 | GitHub + SSH | Enviar o código para o GitHub sem digitar senha |
| 3 | GitHub Actions (Build) | Pipeline que builda a imagem Docker automaticamente |
| 4 | GitHub Actions (Testes) | Pipeline que sobe a app e roda curls de validação |

---

## Milestone 1 — API de usuários + Docker

**Objetivo:** Ter uma API REST de **usuários de um site** funcionando localmente com banco de dados, tudo dentro de containers. Só backend — sem front-end.

**O que é CRUD?** Sigla em inglês para as 4 operações básicas de qualquer sistema que guarda dados no banco:

| Letra | Significado | Neste projeto |
|-------|-------------|---------------|
| **C** | **C**reate (criar) | Cadastrar um novo usuário |
| **R** | **R**ead (ler/consultar) | Fazer login — a API consulta o usuário e valida a senha |
| **U** | **U**pdate (atualizar) | Trocar a senha do usuário |
| **D** | **D**elete (deletar) | Remover a conta do usuário |

**Cenário:** Imagine que você tem um site. O backend precisa cobrir esse CRUD de usuários:

1. **C — Create:** alguém **cria uma conta** (`POST /users`)
2. **R — Read:** alguém **entra no site** com usuário e senha — a API lê os dados e confere se batem (`POST /login`)
3. **U — Update:** alguém **atualiza a senha** (`PUT /users/{id}/password`)
4. **D — Delete:** alguém **encerra a conta** (`DELETE /users/{id}`)

> Sem front-end aqui — você testa tudo com `curl`, como se fosse o site chamando o backend.

### 1.1 — Estrutura do projeto

Crie a pasta do projeto e a estrutura de arquivos:

```
leigo/
├── app/
│   ├── __init__.py
│   ├── main.py          # API FastAPI
│   ├── models.py        # Modelo do banco (SQLAlchemy)
│   ├── database.py      # Conexão com o banco
│   └── schemas.py       # Validação de entrada/saída (Pydantic)
├── scripts/
│   └── validate.sh      # Curls de validação (cadastro, login, senha, delete)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .gitignore
```

**Comandos:**

```bash
mkdir -p leigo/app leigo/scripts
cd leigo
```

### 1.2 — Dependências Python

Crie o arquivo `requirements.txt`:

```
fastapi==0.115.0
uvicorn[standard]==0.30.0
sqlalchemy==2.0.35
psycopg2-binary==2.9.9
fastapi==0.115.0
uvicorn[standard]==0.30.0
sqlalchemy==2.0.35
psycopg2-binary==2.9.9
pydantic==2.9.0
passlib[bcrypt]==1.7.4
```

> **O que é cada coisa (leigo):**
> - **FastAPI** — framework web para criar a API
> - **Uvicorn** — servidor que roda a API
> - **SQLAlchemy** — ORM (traduz Python ↔ SQL)
> - **psycopg2** — driver para conectar no PostgreSQL
> - **Pydantic** — valida os dados que entram e saem da API
> - **passlib** — criptografa a senha antes de salvar no banco (nunca salve senha em texto puro)

### 1.3 — Banco de dados (PostgreSQL)

A app gerencia **usuários** de um site. Campos no banco:

- `id` — identificador único (auto)
- `username` — nome de login (único)
- `password_hash` — senha criptografada (nunca expor na API)

**Endpoints da API:**

| Método | Rota | Ação | Exemplo de uso |
|--------|------|------|----------------|
| GET | `/health` | Verificar se a app está viva | Monitoramento / CI |
| POST | `/users` | **Criar usuário** (cadastro) | Novo visitante se registra no site |
| POST | `/login` | **Entrar** com usuário e senha | Visitante faz login |
| PUT | `/users/{id}/password` | **Atualizar senha** | Usuário troca a senha |
| DELETE | `/users/{id}` | **Deletar usuário** | Usuário encerra a conta |

**Exemplos de request/response:**

```bash
# Cadastro
POST /users
{"username": "joao", "password": "senha123"}
→ {"id": 1, "username": "joao"}

# Login OK
POST /login
{"username": "joao", "password": "senha123"}
→ {"message": "login ok", "user_id": 1, "username": "joao"}

# Login errado
POST /login
{"username": "joao", "password": "errada"}
→ HTTP 401 {"detail": "usuário ou senha inválidos"}

# Atualizar senha
PUT /users/1/password
{"password": "novaSenha456"}
→ {"message": "senha atualizada"}

# Deletar usuário
DELETE /users/1
→ HTTP 204 (sem conteúdo)
```

> **Importante (leigo):** A senha **nunca** volta na resposta da API. No banco fica só o hash.

### 1.4 — Dockerfile

O Dockerfile diz ao Docker **como montar a imagem** da aplicação.

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

> **Leitura do Dockerfile (leigo):**
> 1. `FROM` — começa com Python 3.12
> 2. `WORKDIR` — pasta de trabalho dentro do container
> 3. `COPY` + `RUN pip install` — instala dependências
> 4. `COPY app/` — copia o código da aplicação
> 5. `EXPOSE 8000` — porta que a API usa
> 6. `CMD` — comando que inicia a API quando o container sobe

### 1.5 — Docker Compose

O `docker-compose.yml` sobe **dois containers juntos**: a app e o banco.

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: leigo
      POSTGRES_PASSWORD: leigo123
      POSTGRES_DB: leigo_db
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U leigo -d leigo_db"]
      interval: 5s
      timeout: 5s
      retries: 5

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://leigo:leigo123@db:5432/leigo_db
    depends_on:
      db:
        condition: service_healthy
```

> **Leitura do Compose (leigo):**
> - `db` — container do PostgreSQL com healthcheck (espera o banco ficar pronto)
> - `app` — container da API, builda a partir do Dockerfile
> - `depends_on` — a app só sobe depois que o banco estiver saudável
> - `ports` — mapeia porta do container para sua máquina (8000 = API, 5432 = banco)

### 1.6 — Subir e testar localmente

```bash
# Buildar e subir tudo
docker compose up --build -d

# Ver se os containers estão rodando
docker compose ps

# Ver logs da aplicação
docker compose logs app
```

**Teste manual rápido:**

```bash
# Health check
curl http://localhost:8000/health

# 1. Cadastrar usuário
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "joao", "password": "senha123"}'

# 2. Login
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "joao", "password": "senha123"}'

# 3. Atualizar senha (troque o 1 pelo id retornado no cadastro)
curl -X PUT http://localhost:8000/users/1/password \
  -H "Content-Type: application/json" \
  -d '{"password": "novaSenha456"}'

# 4. Login com senha nova
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "joao", "password": "novaSenha456"}'

# 5. Deletar usuário
curl -X DELETE http://localhost:8000/users/1
```

### 1.7 — Script de validação (curls)

Crie `scripts/validate.sh` — esse script simula o **fluxo completo de um usuário no site**:

```bash
#!/bin/bash
set -e

BASE_URL="${BASE_URL:-http://localhost:8000}"
USERNAME="usuario_teste_$(date +%s)"
PASSWORD="senha123"
NEW_PASSWORD="novaSenha456"

echo "=== 1. Health Check ==="
curl -sf "$BASE_URL/health" | grep -q "ok"
echo "OK"

echo "=== 2. CREATE — Cadastrar usuário ==="
RESPONSE=$(curl -sf -X POST "$BASE_URL/users" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}")
USER_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "Usuário criado: $USERNAME (ID: $USER_ID)"

echo "=== 3. LOGIN — Entrar com senha correta ==="
curl -sf -X POST "$BASE_URL/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}" | grep -q "login ok"
echo "OK"

echo "=== 4. LOGIN — Senha errada deve falhar (401) ==="
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"senha_errada\"}")
[ "$HTTP_CODE" = "401" ] || { echo "Esperava 401, recebeu $HTTP_CODE"; exit 1; }
echo "OK (401 como esperado)"

echo "=== 5. UPDATE — Atualizar senha ==="
curl -sf -X PUT "$BASE_URL/users/$USER_ID/password" \
  -H "Content-Type: application/json" \
  -d "{\"password\": \"$NEW_PASSWORD\"}" | grep -q "senha atualizada"
echo "OK"

echo "=== 6. LOGIN — Entrar com senha nova ==="
curl -sf -X POST "$BASE_URL/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"$NEW_PASSWORD\"}" | grep -q "login ok"
echo "OK"

echo "=== 7. LOGIN — Senha antiga não deve funcionar (401) ==="
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}")
[ "$HTTP_CODE" = "401" ] || { echo "Esperava 401, recebeu $HTTP_CODE"; exit 1; }
echo "OK (401 como esperado)"

echo "=== 8. DELETE — Deletar usuário ==="
curl -sf -X DELETE "$BASE_URL/users/$USER_ID"
echo "OK"

echo "=== 9. LOGIN — Usuário deletado não entra mais (401) ==="
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"$NEW_PASSWORD\"}")
[ "$HTTP_CODE" = "401" ] || { echo "Esperava 401, recebeu $HTTP_CODE"; exit 1; }
echo "OK (401 como esperado)"

echo ""
echo "✅ Todos os testes passaram!"
```

```bash
chmod +x scripts/validate.sh
./scripts/validate.sh
```

### 1.8 — .gitignore

```
__pycache__/
*.pyc
.env
.venv/
```

### ✅ Critério de sucesso — Milestone 1

- [ ] `docker compose up --build` sobe sem erros
- [ ] `curl http://localhost:8000/health` retorna `{"status": "ok"}`
- [ ] `./scripts/validate.sh` passa todos os 9 testes (cadastro → login → senha → delete)
- [ ] `docker compose down` derruba tudo limpo

---

## Milestone 2 — GitHub + SSH

**Objetivo:** Configurar acesso SSH ao GitHub e enviar o repositório.

### 2.1 — Criar repositório no GitHub

1. Acesse [github.com/new](https://github.com/new)
2. Nome: `leigo-crud` (ou o nome que preferir)
3. **Não** marque "Add README" (já temos código local)
4. Clique em **Create repository**

### 2.2 — Gerar chave SSH

```bash
# Gerar par de chaves (substitua o email)
ssh-keygen -t ed25519 -C "seu-email@exemplo.com"

# Quando perguntar o caminho, aperte ENTER (usa o padrão)
# Quando perguntar passphrase, aperte ENTER (sem senha, para CI)
```

### 2.3 — Adicionar chave no GitHub

```bash
# Copiar a chave pública
cat ~/.ssh/id_ed25519.pub
```

1. GitHub → **Settings** (do seu perfil, não do repo)
2. **SSH and GPG keys** → **New SSH key**
3. Title: `meu-laptop` (ou nome da máquina)
4. Key: cole o conteúdo copiado
5. **Add SSH key**

### 2.4 — Testar conexão SSH

```bash
ssh -T git@github.com
```

Resposta esperada: `Hi <seu-usuario>! You've successfully authenticated...`

### 2.5 — Enviar código para o GitHub

```bash
cd leigo

git init
git add .
git commit -m "feat: API de usuários Python com Docker e script de validação"

# Substitua SEU-USUARIO pelo seu username do GitHub
git remote add origin git@github.com:SEU-USUARIO/leigo-crud.git
git branch -M main
git push -u origin main
```

### ✅ Critério de sucesso — Milestone 2

- [ ] `ssh -T git@github.com` autentica com sucesso
- [ ] Código visível no GitHub (todos os arquivos do projeto)
- [ ] `git push` funciona sem pedir senha

---

## Milestone 3 — GitHub Actions (Build)

**Objetivo:** Pipeline que builda a imagem Docker automaticamente a cada push.

### 3.1 — Criar o workflow

Crie o arquivo `.github/workflows/ci.yml`:

```yaml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    name: Build Docker Image
    runs-on: ubuntu-latest

    steps:
      - name: Checkout código
        uses: actions/checkout@v4

      - name: Build imagem Docker
        run: docker build -t leigo-crud:latest .
```

> **Leitura do workflow (leigo):**
> - `on: push` — roda quando alguém faz push na branch `main`
> - `runs-on: ubuntu-latest` — usa uma máquina virtual Ubuntu gratuita do GitHub
> - `actions/checkout@v4` — baixa o código do repositório
> - `docker build` — builda a imagem Docker (mesmo comando que rodamos local)

### 3.2 — Enviar e verificar

```bash
git add .github/workflows/ci.yml
git commit -m "ci: adiciona pipeline de build Docker"
git push
```

**Verificar no GitHub:**
1. Vá no repositório → aba **Actions**
2. Clique no workflow que rodou
3. Deve aparecer ✅ verde com "Build Docker Image" passando

### ✅ Critério de sucesso — Milestone 3

- [ ] Push dispara o workflow automaticamente
- [ ] Job "Build Docker Image" fica verde (✅)
- [ ] Logs mostram `Successfully built` ou similar

---

## Milestone 4 — GitHub Actions (Validação com Curls)

**Objetivo:** Pipeline que sobe a app completa (app + banco) e roda os curls de validação.

### 4.1 — Atualizar o workflow

Substitua o conteúdo de `.github/workflows/ci.yml`:

```yaml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    name: Build + Validar API de usuários
    runs-on: ubuntu-latest

    steps:
      - name: Checkout código
        uses: actions/checkout@v4

      - name: Build e subir containers
        run: docker compose up --build -d

      - name: Aguardar app ficar pronta
        run: |
          echo "Aguardando API..."
          for i in $(seq 1 30); do
            if curl -sf http://localhost:8000/health; then
              echo "App pronta!"
              exit 0
            fi
            echo "Tentativa $i/30..."
            sleep 2
          done
          echo "App não respondeu a tempo"
          docker compose logs
          exit 1

      - name: Rodar validação (cadastro, login, senha, delete)
        run: ./scripts/validate.sh

      - name: Mostrar logs (se falhar)
        if: failure()
        run: docker compose logs

      - name: Derrubar containers
        if: always()
        run: docker compose down -v
```

> **O que mudou (leigo):**
> - Agora sobe **app + banco** com `docker compose up`
> - **Espera** a API responder (loop de retry por até 60 segundos)
> - **Roda** o script `validate.sh` com todos os curls
> - Se falhar, **mostra os logs** para debug
> - **Sempre derruba** os containers no final (`if: always()`)

### 4.2 — Enviar e verificar

```bash
git add .github/workflows/ci.yml
git commit -m "ci: adiciona validação da API de usuários com curls no pipeline"
git push
```

**Verificar no GitHub:**
1. Aba **Actions** → clique no workflow mais recente
2. Expanda os steps e confira:
   - ✅ Build e subir containers
   - ✅ Aguardar app ficar pronta
   - ✅ Rodar validação (cadastro, login, senha, delete)
3. Nos logs do step de validação, deve aparecer: `✅ Todos os testes passaram!`

### 4.3 — Testar que a pipeline pega erros

Para provar que a validação funciona de verdade, faça um teste proposital:

1. Quebre algo na API (ex: mude a rota `/health` para `/healthz`)
2. Faça push
3. A pipeline deve falhar ❌ no step de validação
4. Reverta a mudança e confirme que volta a passar ✅

### ✅ Critério de sucesso — Milestone 4

- [ ] Pipeline sobe app + banco automaticamente
- [ ] Script `validate.sh` roda dentro do CI
- [ ] Pipeline fica verde quando a app está OK
- [ ] Pipeline fica vermelha quando a app está quebrada
- [ ] Logs são exibidos quando algo falha

---

## Resumo final — O que foi aprendido

```
┌─────────────────────────────────────────────────────────┐
│                    FLUXO COMPLETO                       │
│                                                         │
│  Código Python  →  Dockerfile  →  Docker Compose        │
│       ↓                                                 │
│  git push (SSH)  →  GitHub                              │
│       ↓                                                 │
│  GitHub Actions  →  Build  →  Sobe containers           │
│       ↓                                                 │
│  validate.sh (curls)  →  ✅ ou ❌                         │
└─────────────────────────────────────────────────────────┘
```

| Conceito | O que é |
|----------|---------|
| **API REST** | Backend que responde HTTP — aqui gerencia usuários do site |
| **Cadastro / Login** | Criar conta e autenticar com usuário + senha |
| **Hash de senha** | Senha criptografada no banco; a API nunca devolve a senha |
| **Dockerfile** | Receita para criar a imagem da aplicação |
| **Docker Compose** | Orquestra múltiplos containers (app + banco) |
| **SSH Key** | Chave de acesso seguro ao GitHub (sem senha) |
| **GitHub Actions** | CI/CD — automação que roda a cada push |
| **Health Check** | Endpoint que confirma se a app está viva |
| **validate.sh** | Testes automatizados com curl simulando um usuário real |

---

## Próximos passos (opcional, pós-roadmap)

Quando dominar as 4 milestones, evolua para:

1. **Deploy** — publicar a app em um servidor (AWS, Railway, Fly.io)
2. **Secrets** — mover senhas do banco para variáveis de ambiente seguras
3. **Linting** — adicionar `ruff` ou `flake8` no pipeline
4. **Coverage** — testes unitários com `pytest`
5. **Multi-stage build** — Dockerfile otimizado (imagem menor)
6. **Branch protection** — exigir pipeline verde antes de merge

---

## Troubleshooting comum

| Problema | Solução |
|----------|---------|
| `docker compose up` falha no banco | Espere 10s e tente de novo; o healthcheck resolve na 2ª tentativa |
| `Permission denied (publickey)` no push | Chave SSH não configurada — refaça Milestone 2 |
| Pipeline timeout no health check | App demorou para subir; aumente o loop de retry |
| `curl: command not found` no CI | Ubuntu do GitHub já tem curl; verifique se o script tem `#!/bin/bash` |
| Login retorna 401 sempre | Confira se a senha está sendo hasheada na criação e comparada no login |
| Username duplicado | Cadastro deve retornar HTTP 409 se o usuário já existir |
| Porta 8000 já em uso | `docker compose down` ou mate o processo: `lsof -i :8000` |