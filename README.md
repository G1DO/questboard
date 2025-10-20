# QuestBoard

A gamified “micro-challenges” platform built with **Flask**. Users register, join quests, submit proof, and climb a weekly leaderboard.

* Backend: Flask + SQLAlchemy + Alembic (Flask-Migrate)
* Auth: JWT (HttpOnly cookies) via Flask-JWT-Extended
* Frontend: Jinja templates + vanilla JS
* DB: Postgres (Docker) or SQLite (local dev)
* Container: Docker + Gunicorn
* Deploy-ready: image published on Docker Hub

---

## Table of Contents

* [Tech Stack](#tech-stack)
* [Run with Docker (recommended)](#run-with-docker-recommended)
* [Run locally without Docker](#run-locally-without-docker)
* [Environment Variables](#environment-variables)
* [Database & Migrations](#database--migrations)
* [API Endpoints](#api-endpoints)
* [Basic UI Pages](#basic-ui-pages)
* [Docker Image (push/pull)](#docker-image-pushpull)
* [Project Structure](#project-structure)

---

## Tech Stack

* **Flask**, **Flask-SQLAlchemy**, **SQLAlchemy**
* **Alembic / Flask-Migrate**
* **Flask-JWT-Extended**, **Flask-CORS**, **Pydantic**, **email-validator**, **Werkzeug**
* **Postgres** (Docker) or **SQLite**
* **Gunicorn**, **Docker**, **Docker Compose**

---

## Run with Docker (recommended)

### 1) Prereqs

* Docker Desktop (Win/macOS) or Docker Engine + Compose (Linux)
* Git

### 2) Clone & configure

```bash
git clone https://github.com/G1DO/questboard
cd questboard
cp .env.example .env
# edit SECRET_KEY in .env to a long random value
# python -c "import secrets; print(secrets.token_urlsafe(64))"
```

### 3) Start with Postgres via Compose

```bash
docker compose pull
docker compose up -d
```

Open:

* API health: [http://localhost:8000/health](http://localhost:8000/health)
* Home: [http://localhost:8000/](http://localhost:8000/)

---

## Run locally without Docker

### 1) Create venv & install

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS/WSL:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2) Environment

```bash
cp .env.example .env
# For local dev:
# FLASK_ENV=development
# SECRET_KEY=<random-secret>
```

### 3) DB (SQLite by default)

```bash
flask --app wsgi.py db upgrade
python wsgi.py
```

Open: [http://localhost:8000](http://localhost:8000)

---

## Environment Variables

`./.env` (loaded by Docker via `env_file`, and by Python if you `load_dotenv`):

* `FLASK_ENV` — `production` in Docker, `development` locally for debug
* `SECRET_KEY` — long, random, **required** (used to sign cookies/JWTs)
* `DATABASE_URL` — override DB (Compose sets it for Postgres)

Example:

```env
FLASK_ENV=production
SECRET_KEY=<paste-a-random-secret>
# DATABASE_URL=postgresql+psycopg://quest:quest@db:5432/questdb
```

---

## Database & Migrations

* Create/upgrade schema:

```bash
flask --app wsgi.py db upgrade
```

* After model changes:

```bash
flask --app wsgi.py db migrate -m "describe change"
flask --app wsgi.py db upgrade
```

* In Docker:

```bash
docker compose run --rm web flask db migrate -m "..."
docker compose run --rm web flask db upgrade
```

---

## API Endpoints

Base URL: `/api`

| Method | Path                                   | Body (JSON)                                                                                       | Response (example)                            |
| -----: | -------------------------------------- | ------------------------------------------------------------------------------------------------- | --------------------------------------------- |
|   POST | `/auth/register`                       | `{"email":"dev@me.com","display_name":"Dev","password":"secret123"}`                              | `{"id":1,"email":"...","display_name":"..."}` |
|   POST | `/auth/login`                          | `{"email":"dev@me.com","password":"secret123"}`                                                   | `{ "access_token": "...", "user": {...} }`    |
|    GET | `/auth/me` (JWT)                       | —                                                                                                 | Current user                                  |
|   POST | `/auth/logout` (JWT)                   | —                                                                                                 | `{ "msg": "logged out" }`                     |
|    GET | `/quests`                              | —                                                                                                 | `[ ...quests ]`                               |
|   POST | `/quests`                              | `{"title":"...","description":"...","starts_on":"YYYY-MM-DD","ends_on":"YYYY-MM-DD","points":10}` | `{ "id": <quest_id> }`                        |
|   POST | `/submissions`                         | `{"user_id":1,"quest_id":1,"text":"Finished!","image_url":null}`                                  | `{ "id":..., "status":"pending" }`            |
|   POST | `/submissions/<submission_id>/approve` | —                                                                                                 | `{ "id":..., "status":"approved" }`           |
|    GET | `/leaderboard`                         | —                                                                                                 | `[{"user":"Alice","points":15}, ...]`         |

Notes:

* Dates are ISO `YYYY-MM-DD`.
* Points are awarded **only when a submission is approved**.

---

## Basic UI Pages

Server-rendered pages (Jinja):

* `/` Home
* `/register` Register
* `/login` Login
* `/quests` List quests + create submission
* `/leaderboard` Weekly leaderboard

---

## Docker Image (push/pull)

The app image is published at:

```
g1d0/questboard-web:v0.1.0
g1d0/questboard-web:latest
```

Use in Compose:

```yaml
web:
  image: g1d0/questboard-web:v0.1.0
  env_file: .env
  environment:
    DATABASE_URL: postgresql+psycopg://quest:quest@db:5432/questdb
    FLASK_ENV: production
  ports: ["8000:8000"]
  depends_on:
    db:
      condition: service_healthy
```

Pull & run anywhere:

```bash
docker login
docker compose pull
docker compose up -d
```

---

## Project Structure

```
questboard/
├─ app/
│  ├─ __init__.py        # App factory: config, extensions, blueprints
│  ├─ routes.py          # / and /health
│  ├─ pages.py           # Jinja page routes
│  ├─ api.py             # /api/* core endpoints
│  ├─ auth.py            # /auth/* (JWT cookies)
│  ├─ models.py          # SQLAlchemy models
│  ├─ schemas.py         # Pydantic validators
│  ├─ extensions.py      # db, migrate singletons
│  ├─ templates/         # Jinja templates
│  └─ static/            # CSS/JS
├─ migrations/           # Alembic
├─ instance/             # runtime data (gitignored)
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
├─ .env.example
└─ README.md
```