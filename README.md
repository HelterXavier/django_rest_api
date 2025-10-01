# Dajngo Backend Setup API

API RESTful construída com Django e Django REST Framework para o projeto Mergetune.

## Funcionalidades

- Autenticação de usuários com JWT (JSON Web Tokens).
- Criação e gerenciamento de contas de usuário.
- Atualização de perfil e alteração de senha.
- Endpoint de health check para monitoramento.

## Tecnologias Utilizadas

- **Backend:** Django, Django REST Framework
- **Banco de Dados:** PostgreSQL
- **Autenticação:** djangorestframework-simplejwt
- **Containerização:** Docker, Docker Compose

---

## Como Executar o Projeto

### Pré-requisitos

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Configuração do Ambiente

Na raiz do projeto, crie um arquivo chamado `.env` e preencha com as suas credenciais. Você pode usar o arquivo `.env.example` como base.

```bash
# .env

# Configurações do Django
DJANGO_SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Configurações do Banco de Dados PostgreSQL
POSTGRES_DB=mergetune_db
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
DJANGO_DB_NAME=mergetune_db
DJANGO_DB_HOST=db
DJANGO_DB_PORT=5432
```

### 2. Build e Execução dos Containers

Execute o comando abaixo na raiz do projeto para construir as imagens e iniciar os serviços:

```bash
docker-compose up --build -d
```

### 3. Executar Migrações do Banco de Dados

Após os containers estarem em execução, aplique as migrações do Django:

```bash
docker-compose exec backend python manage.py migrate
```

A API estará disponível em `http://localhost:8000`.

---

## Documentação da API

### Health Check

Endpoint para verificar se a API está online.

#### `GET /`

- **Descrição:** Retorna uma página HTML simples confirmando que a API está em execução.
- **Autenticação:** Nenhuma.
- **Resposta de Sucesso (200 OK):**
  ```html
  <!-- Conteúdo HTML da página de status -->
  ```

### Autenticação (JWT)

#### `POST /api/token/`

- **Descrição:** Autentica um usuário e retorna um par de tokens (acesso e atualização).
- **Autenticação:** Nenhuma.
- **Corpo da Requisição (JSON):**
  ```json
  {
    "email": "seu-email@exemplo.com",
    "password": "sua-senha"
  }
  ```
- **Resposta de Sucesso (200 OK):**
  ```json
  {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```

#### `POST /api/token/refresh/`

- **Descrição:** Gera um novo token de acesso usando um token de atualização (refresh token) válido.
- **Autenticação:** Nenhuma.
- **Corpo da Requisição (JSON):**
  ```json
  {
    "refresh": "seu-refresh-token-aqui"
  }
  ```
- **Resposta de Sucesso (200 OK):**
  ```json
  {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```

#### `POST /api/logout/`

- **Descrição:** Invalida um token de atualização, efetivamente fazendo o logout do usuário.
- **Autenticação:** Requer token de acesso (`Bearer <token>`).
- **Corpo da Requisição (JSON):**
  ```json
  {
    "refresh": "seu-refresh-token-aqui"
  }
  ```
- **Resposta de Sucesso (205 Reset Content):**
  ```json
  {
    "detail": "Logout successful"
  }
  ```

### Gerenciamento de Usuários

#### `POST /api/`

- **Descrição:** Cria uma nova conta de usuário.
- **Autenticação:** Nenhuma.
- **Corpo da Requisição (JSON):**
  ```json
  {
    "name": "Nome Completo",
    "username": "nome_de_usuario",
    "email": "seu-email@exemplo.com",
    "password": "senha-forte",
    "password2": "senha-forte"
  }
  ```
- **Resposta de Sucesso (201 Created):**
  ```json
  {
    "detail": "Account created successfully."
  }
  ```

#### `GET /api/me/`

- **Descrição:** Retorna as informações do usuário atualmente autenticado.
- **Autenticação:** Requer token de acesso (`Bearer <token>`).
- **Resposta de Sucesso (200 OK):**
  ```json
  {
    "id": 1,
    "name": "Nome Completo",
    "username": "nome_de_usuario",
    "email": "seu-email@exemplo.com",
    "instruments": "Guitarra",
    "photo": "/media/user_photos/foto.jpg"
  }
  ```

#### `PATCH /api/me/`

- **Descrição:** Atualiza uma ou mais informações do usuário autenticado.
- **Autenticação:** Requer token de acesso (`Bearer <token>`).
- **Corpo da Requisição (JSON):** (Envie apenas os campos que deseja alterar)
  ```json
  {
    "name": "Novo Nome",
    "instruments": "Baixo, Bateria"
  }
  ```
- **Resposta de Sucesso (200 OK):** Retorna o objeto do usuário com os dados atualizados.

#### `PATCH /api/password/`

- **Descrição:** Permite que o usuário autenticado altere sua própria senha.
- **Autenticação:** Requer token de acesso (`Bearer <token>`).
- **Corpo da Requisição (JSON):**
  ```json
  {
    "current_password": "senha-atual",
    "new_password": "nova-senha-forte",
    "new_password2": "nova-senha-forte"
  }
  ```
- **Resposta de Sucesso (200 OK):**
  ```json
  {
    "detail": "Password updated successfully."
  }
  ```
