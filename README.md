# 🧭 QuestBoard

A gamified “micro-challenges” platform built with **Flask**.
Users register, join quests, submit proof, and climb a weekly leaderboard.

---

## 🚀 Key Features

* Backend: **Flask + SQLAlchemy + Alembic (Flask-Migrate)**
* Authentication: **JWT (HttpOnly cookies)** via Flask-JWT-Extended
* Frontend: **Jinja templates + Vanilla JS**
* Database: **Postgres (Docker)** or **SQLite (local dev)**
* Containerization: **Docker + Gunicorn**
* CI/CD Ready: **Elastic Beanstalk (EB CLI) auto-deploy**
* **Live HTTPS Deployment** via AWS CloudFront + ACM Certificate

---

## 📦 Table of Contents

1. [Live Deployment](#-live-deployment)
2. [Tech Stack](#-tech-stack)
3. [Run with Docker (Recommended)](#-run-with-docker-recommended)
4. [Run Locally (Without Docker)](#-run-locally-without-docker)
5. [Environment Variables](#-environment-variables)
6. [Database & Migrations](#-database--migrations)
7. [API Endpoints](#-api-endpoints)
8. [Basic UI Pages](#️-basic-ui-pages)
9. [Docker Image (Push / Pull)](#-docker-image-push--pull)
10. [Project Structure](#️-project-structure)

---

## 🌍 Live Deployment

QuestBoard is live and secured with HTTPS through AWS infrastructure:

| Component               | Service                                    |
| ----------------------- | ------------------------------------------ |
| **Application Hosting** | AWS Elastic Beanstalk (Docker environment) |
| **Load Balancer**       | Application Load Balancer (ALB)            |
| **CDN / HTTPS**         | Amazon CloudFront                          |
| **SSL Certificate**     | AWS Certificate Manager (ACM)              |
| **Region**              | eu-north-1 (Stockholm)                     |

**Live URL:**
👉 [Live Demo](https://d277uiwpvrg0wk.cloudfront.net/)

---

## 🧠 Tech Stack

| Layer          | Technology                                      |
| -------------- | ----------------------------------------------- |
| Backend        | Flask, Flask-SQLAlchemy, Alembic, Flask-Migrate |
| Authentication | Flask-JWT-Extended, Flask-CORS                  |
| Validation     | Pydantic, email-validator                       |
| Database       | PostgreSQL (Docker) / SQLite (local)            |
| Deployment     | Docker, Elastic Beanstalk, CloudFront           |
| Web Server     | Gunicorn                                        |
| Config         | `.env`, `Dockerrun.aws.json`, `.ebextensions/`  |

---

## 🐳 Run with Docker (Recommended)

### 1️⃣ Prerequisites

* Docker Desktop (Windows/macOS) or Docker Engine + Compose (Linux)
* Git

### 2️⃣ Clone & Configure

```bash
git clone https://github.com/G1DO/questboard
cd questboard
cp .env.example .env
# Generate a secure key:
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

### 3️⃣ Start Containers

```bash
docker compose pull
docker compose up -d
```

Access:

* API Health → [http://localhost:8000/health](http://localhost:8000/health)
* Web App → [http://localhost:8000](http://localhost:8000)

---

## 💻 Run Locally (Without Docker)

### 1️⃣ Setup Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

### 2️⃣ Configure Environment

```bash
cp .env.example .env
# Example:
# FLASK_ENV=development
# SECRET_KEY=<your-secret>
```

### 3️⃣ Initialize Database

```bash
flask --app wsgi.py db upgrade
python wsgi.py
```

Then open → [http://localhost:8000](http://localhost:8000)

---

## ⚙️ Environment Variables

Environment file: `.env`
(loaded automatically by Flask and Docker)

| Variable       | Description                                   |
| -------------- | --------------------------------------------- |
| `FLASK_ENV`    | `production` or `development`                 |
| `SECRET_KEY`   | Required for JWT and cookies                  |
| `DATABASE_URL` | Optional, overrides default DB                |
| `PORT`         | Default 8000 (Elastic Beanstalk auto-detects) |

Example:

```env
FLASK_ENV=production
SECRET_KEY=<your-secret>
# DATABASE_URL=postgresql+psycopg://quest:quest@db:5432/questdb
```

---

## 🧩 Database & Migrations

Run migrations manually:

```bash
flask --app wsgi.py db migrate -m "add new model"
flask --app wsgi.py db upgrade
```

Or inside Docker:

```bash
docker compose run --rm web flask db migrate -m "..."
docker compose run --rm web flask db upgrade
```

---

## 🔗 API Endpoints

Base URL: `/api`

| Method | Endpoint                    | Body                                                                 | Description        |
| ------ | --------------------------- | -------------------------------------------------------------------- | ------------------ |
| POST   | `/auth/register`            | `{"email":"dev@me.com","display_name":"Dev","password":"secret123"}` | Create new user    |
| POST   | `/auth/login`               | `{"email":"dev@me.com","password":"secret123"}`                      | Authenticate user  |
| GET    | `/auth/me`                  | —                                                                    | Get current user   |
| POST   | `/auth/logout`              | —                                                                    | Logout user        |
| GET    | `/quests`                   | —                                                                    | List quests        |
| POST   | `/quests`                   | Quest JSON                                                           | Create new quest   |
| POST   | `/submissions`              | Submission JSON                                                      | Submit proof       |
| POST   | `/submissions/<id>/approve` | —                                                                    | Approve submission |
| GET    | `/leaderboard`              | —                                                                    | Weekly leaderboard |

---

## 🖥️ Basic UI Pages

| Route          | Description             |
| -------------- | ----------------------- |
| `/`            | Home                    |
| `/register`    | Register page           |
| `/login`       | Login page              |
| `/quests`      | Quest list + submission |
| `/leaderboard` | Leaderboard view        |

---

## 🐙 Docker Image (Push / Pull)

App images on Docker Hub:

```
g1d0/questboard-web:latest
```

Use in `docker-compose.yml`:

```yaml
web:
  image: g1d0/questboard-web:latest
  env_file: .env
  environment:
    DATABASE_URL: postgresql+psycopg://quest:quest@db:5432/questdb
    FLASK_ENV: production
  ports:
    - "8000:8000"
  depends_on:
    db:
      condition: service_healthy
```

---

## 🗂️ Project Structure

```
questboard/
├─ .ebextensions/
│  └─ 01_port.config          # Maps container port 8000 for Elastic Beanstalk
├─ .elasticbeanstalk/         # EB environment & deployment metadata
├─ app/
│  ├─ __init__.py             # App factory: config, blueprints
│  ├─ routes.py               # / and /health
│  ├─ pages.py                # Jinja routes
│  ├─ api.py                  # API endpoints
│  ├─ auth.py                 # JWT auth routes
│  ├─ models.py               # SQLAlchemy models
│  ├─ schemas.py              # Pydantic validators
│  ├─ extensions.py           # db, migrate
│  ├─ templates/              # Jinja templates
│  └─ static/                 # JS / CSS
├─ migrations/                # Alembic versions
├─ instance/                  # Runtime data (gitignored)
├─ Dockerfile                 # Flask + Gunicorn container
├─ docker-compose.yml         # Local multi-container setup
├─ Dockerrun.aws.json         # AWS Elastic Beanstalk Docker config
├─ requirements.txt           # Dependencies
├─ .env.example               # Env template
├─ wsgi.py                    # Entry point for Gunicorn
├─ README.md
└─ misc/                      # Other project files (.gitignore, .dockerignore, etc.)
```
