# 🧭 QuestBoard

A gamified “micro-challenges” platform built with **Flask**.
Users register, join quests, submit proof, and climb a weekly leaderboard.

---

## 🚀 Key Features

* Backend: **Flask + SQLAlchemy + Alembic (Flask-Migrate)**
* Authentication: **JWT (HttpOnly cookies)** via Flask-JWT-Extended
* Frontend: **Jinja templates + Vanilla JS**
* Database: **AWS RDS PostgreSQL (Production)** / **Docker PostgreSQL or SQLite (Local)**
* Containerization: **Docker + Gunicorn**
* CI/CD: **AWS Elastic Beanstalk (EB CLI) auto-deploy**
* HTTPS: **AWS CloudFront + ACM Certificate**

---

## 📦 Table of Contents

1. [Live Deployment](#-live-deployment)
2. [AWS PostgreSQL Setup](#-aws-postgresql-setup)
3. [Tech Stack](#-tech-stack)
4. [Run with Docker (Recommended)](#-run-with-docker-recommended)
5. [Run Locally (Without Docker)](#-run-locally-without-docker)
6. [Environment Variables](#-environment-variables)
7. [Database & Migrations](#-database--migrations)
8. [API Endpoints](#-api-endpoints)
9. [Basic UI Pages](#️-basic-ui-pages)
10. [Docker Image (Push / Pull)](#-docker-image-push--pull)
11. [Project Structure](#️-project-structure)

---

## 🌍 Live Deployment

QuestBoard is live and secured with HTTPS through AWS infrastructure:

| Component               | Service                                    |
| ----------------------- | ------------------------------------------ |
| **Application Hosting** | AWS Elastic Beanstalk (Docker environment) |
| **Database**            | **AWS RDS – PostgreSQL 16**                |
| **CDN / HTTPS**         | Amazon CloudFront                          |
| **SSL Certificate**     | AWS Certificate Manager (ACM)              |
| **Region**              | eu-north-1 (Stockholm)                     |

**Live URL:**
[Live Demo](https://d277uiwpvrg0wk.cloudfront.net/)


---

## 🗄️ AWS PostgreSQL Setup

Production uses **Amazon RDS PostgreSQL** instead of Dockerized Postgres.

**Configuration Summary:**

| Setting             | Example                                                   |
| ------------------- | --------------------------------------------------------- |
| **Engine**          | PostgreSQL 16                                             |
| **DB Name**         | `questdb`                                                 |
| **Master Username** | `questdb`                                                 |
| **Endpoint**        | `questboard-db.cpioco0eyxc1.eu-north-1.rds.amazonaws.com` |
| **Port**            | `5432`                                                    |
| **Security Group**  | Allows inbound traffic from Elastic Beanstalk instance    |
| **Parameter Group** | Default (UTF8 encoding)                                   |

**Connection string used in `.env`:**

```bash
DATABASE_URL=postgresql+psycopg2://questdb:<your-password>@questboard-db.cpioco0eyxc1.eu-north-1.rds.amazonaws.com:5432/postgres
```

---

## 🧠 Tech Stack

| Layer      | Technology                                                      |
| ---------- | --------------------------------------------------------------- |
| Backend    | Flask, Flask-SQLAlchemy, Alembic                                |
| Auth       | Flask-JWT-Extended, Flask-CORS                                  |
| Validation | Pydantic, email-validator                                       |
| Database   | **AWS RDS PostgreSQL (prod)** / Docker Postgres or SQLite (dev) |
| Deployment | Docker, Elastic Beanstalk, CloudFront                           |
| Web Server | Gunicorn                                                        |
| Config     | `.env`, `Dockerrun.aws.json`, `.ebextensions/`                  |

---

## 🐳 Run with Docker (Recommended for Local Development)

### 1️⃣ Prerequisites

* Docker Desktop (Windows/macOS) or Compose (Linux)
* Git

### 2️⃣ Clone & Configure

```bash
git clone https://github.com/G1DO/questboard
cd questboard
cp .env.example .env
```

### 3️⃣ Start Containers

```bash
docker compose up -d
```

Access:

* Web → [http://localhost:8000](http://localhost:8000)
* API Health → [http://localhost:8000/health](http://localhost:8000/health)

---

## 💻 Run Locally (Without Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask --app wsgi.py db upgrade
python wsgi.py
```

---

## ⚙️ Environment Variables

| Variable       | Description                   |
| -------------- | ----------------------------- |
| `FLASK_ENV`    | `development` or `production` |
| `SECRET_KEY`   | JWT & cookies                 |
| `DATABASE_URL` | RDS connection string         |
| `PORT`         | Default 8000                  |

Example:

```env
FLASK_ENV=production
SECRET_KEY=<your-secret>
DATABASE_URL=postgresql+psycopg2://questdb:<password>@questboard-db.cpioco0eyxc1.eu-north-1.rds.amazonaws.com:5432/postgres
```

---

## 🧩 Database & Migrations

Run migrations manually:

```bash
flask --app wsgi.py db migrate -m "init"
flask --app wsgi.py db upgrade
```

Or inside Docker:

```bash
docker compose run --rm web flask db migrate -m "init"
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

App image on Docker Hub:

```
g1d0/questboard-web:latest
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
└─ README.md
```