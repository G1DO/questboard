# QuestBoard

This repository provides a minimal Flask application skeleton, achieving **Milestone 1** with database integration and API functionality.

## Technology Stack
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Migrate (powered by Alembic)
- python-dotenv
- SQLite (for development)

---

## Quickstart: Launching the Server (Milestone 0)

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   ```
   - For Windows (Command Prompt): `.venv\Scripts\activate`
   - For Windows (PowerShell): `. .\.venv\Scripts\Activate.ps1`
   - For Linux, macOS, or WSL: `source .venv/bin/activate`

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```

4. Run the development server:
   ```bash
   python wsgi.py
   ```
   The application is accessible at: http://localhost:8000

5. Perform a basic verification in a web browser:
   - http://localhost:8000/ → `{"app":"QuestBoard","message":"Welcome!"}`
   - http://localhost:8000/health → `{"status":"ok"}`

## Milestone 1: Database, Models, Migrations, and Basic API

1. Add additional dependencies if not already present in `requirements.txt`, then reinstall:
   ```
   Flask-SQLAlchemy==3.1.1
   SQLAlchemy==2.0.36
   alembic==1.13.2
   Flask-Migrate==4.0.7
   python-dotenv==1.0.1
   ```
   ```bash
   pip install -r requirements.txt
   ```

2. Initialize the database and create the schema (ensure the server is stopped):
   ```bash
   flask --app wsgi.py db init
   flask --app wsgi.py db migrate -m "init tables"
   flask --app wsgi.py db upgrade
   ```
   This process generates the `migrations/` directory and the `instance/app.db` file.

3. Restart the server:
   ```bash
   python wsgi.py
   ```

4. Conduct integration tests (in a separate terminal while the server is running):
   ```bash
   # Create a user
   curl -X POST http://localhost:8000/api/users \
     -H "Content-Type: application/json" \
     -d '{"email":"a@b.com","display_name":"Alice"}'

   # Create a quest
   curl -X POST http://localhost:8000/api/quests \
     -H "Content-Type: application/json" \
     -d '{"title":"Read 30 pages","description":"Any book","starts_on":"2025-09-22","ends_on":"2025-09-28","points":15}'

   # Create a submission
   curl -X POST http://localhost:8000/api/submissions \
     -H "Content-Type: application/json" \
     -d '{"user_id":1,"quest_id":1,"text":"Finished!"}'

   # Approve a submission (awards points)
   curl -X POST http://localhost:8000/api/submissions/1/approve

   # Retrieve the leaderboard (for the current week)
   curl http://localhost:8000/api/leaderboard
   ```
   Note: On Windows PowerShell, escape quotes using backticks, or utilize tools such as Postman or Insomnia for API testing.

## API Documentation (Milestone 1)
Base URL: http://localhost:8000/api

| Method | Path                          | Request Body (JSON)                                      | Response Example                          |
|--------|-------------------------------|----------------------------------------------------------|-------------------------------------------|
| POST   | /users                        | `{"email":"a@b.com","display_name":"Alice"}`             | `{"id": <user_id>, "email": "...", "display_name": "..."}` |
| GET    | /quests                       | —                                                        | `[ ...quests ]`                           |
| POST   | /quests                       | `{"title":"...","description":"...","starts_on":"YYYY-MM-DD","ends_on":"YYYY-MM-DD","points":10}` | `{"id": <quest_id>}`                      |
| POST   | /submissions                  | `{"user_id":1,"quest_id":1,"text":"Finished!","image_url":null}` | `{"id":...,"status":"pending"}`           |
| POST   | /submissions/<submission_id>/approve | —                                                        | `{"id":...,"status":"approved"}`          |
| GET    | /leaderboard                  | —                                                        | `[{"user":"Alice","points":15}, ...]`     |

Notes:
- Dates must adhere to the ISO format: YYYY-MM-DD.
- Points are awarded to users only upon approval of a submission.

## Configuration
Copy `.env.example` to `.env` and customize as needed:

```
FLASK_ENV=development
SECRET_KEY=change-me
# DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/questboard  # For production use
```
By default, the application uses SQLite at `instance/app.db` (the `instance/` directory is automatically created and ignored by Git).

## Development Workflow
- If models are modified:
  ```bash
  flask --app wsgi.py db migrate -m "describe change"
  flask --app wsgi.py db upgrade
  ```
- For a new installation or an empty database:
  ```bash
  flask --app wsgi.py db upgrade
  ```
- If no schema changes are required, simply run:
  ```bash
  python wsgi.py
  ```

## Troubleshooting
- If encountering an "application context" error, ensure `--app wsgi.py` is included in Flask database commands.
- If a migration file is empty, verify that models are imported correctly in the application (via `app/__init__.py`).
- If SQLite reports a locked database, stop the server, execute migrations, and restart.
- For quoting issues on Windows, consider using Postman, Insomnia, or a WSL terminal.

## Project Structure
```
questboard/
├─ app/
│  ├─ __init__.py          # Application factory (initializes database, migrations, registers routes and API)
│  ├─ routes.py            # Handles root ("/") and health ("/health") endpoints
│  ├─ api.py               # Manages /api/* endpoints
│  ├─ models.py            # Defines SQLAlchemy models
│  ├─ config.py            # Environment-based configuration (defaults to SQLite)
│  └─ extensions.py        # Initializes database and migration extensions
├─ migrations/             # Alembic migration files
├─ instance/               # Runtime files (gitignored) — includes app.db, uploads, etc.
├─ wsgi.py                 # Development entry point (replace with Gunicorn for production)
├─ requirements.txt
├─ .env.example
├─ .gitignore
└─ README.md
```