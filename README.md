````md
# QuestBoard

This repository provides a minimal Flask application skeleton, achieving **Milestone 1** with database integration and API functionality, and **Milestone 2** with authentication, validation, and CORS.

## Technology Stack
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Migrate (powered by Alembic)
- python-dotenv
- SQLite (for development)
- **Milestone 2:** Flask-JWT-Extended, Flask-CORS, Pydantic, email-validator, Werkzeug

---

## Quickstart: Launching the Server (Milestone 0)

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
````

* For Windows (Command Prompt): `.venv\Scripts\activate`
* For Windows (PowerShell): `. .\.venv\Scripts\Activate.ps1`
* For Linux, macOS, or WSL: `source .venv/bin/activate`

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

   The application is accessible at: [http://localhost:8000](http://localhost:8000)

5. Perform a basic verification in a web browser:

   * [http://localhost:8000/](http://localhost:8000/) → `{"app":"QuestBoard","message":"Welcome!"}`
   * [http://localhost:8000/health](http://localhost:8000/health) → `{"status":"ok"}`

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

Base URL: [http://localhost:8000/api](http://localhost:8000/api)

| Method | Path                                   | Request Body (JSON)                                                                               | Response Example                                           |
| ------ | -------------------------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| POST   | /users                                 | `{"email":"a@b.com","display_name":"Alice"}`                                                      | `{"id": <user_id>, "email": "...", "display_name": "..."}` |
| GET    | /quests                                | —                                                                                                 | `[ ...quests ]`                                            |
| POST   | /quests                                | `{"title":"...","description":"...","starts_on":"YYYY-MM-DD","ends_on":"YYYY-MM-DD","points":10}` | `{"id": <quest_id>}`                                       |
| POST   | /submissions                           | `{"user_id":1,"quest_id":1,"text":"Finished!","image_url":null}`                                  | `{"id":...,"status":"pending"}`                            |
| POST   | /submissions/\<submission\_id>/approve | —                                                                                                 | `{"id":...,"status":"approved"}`                           |
| GET    | /leaderboard                           | —                                                                                                 | `[{"user":"Alice","points":15}, ...]`                      |

Notes:

* Dates must adhere to the ISO format: YYYY-MM-DD.
* Points are awarded to users only upon approval of a submission.

---

## Milestone 2: Authentication (JWT HttpOnly Cookies), Validation, and CORS

1. **Add dependencies** (append to `requirements.txt`), then reinstall:

   ```
   Flask-JWT-Extended==4.6.0
   Flask-Cors==4.0.1
   pydantic==2.9.2
   email-validator==2.2.0
   Werkzeug==3.0.4
   ```

   ```bash
   pip install -r requirements.txt
   ```

2. **Model update** (`users.password_hash`) and migration:

   * Add `password_hash = db.Column(db.String(255))` to `User`.
   * Run:

     ```bash
     flask --app wsgi.py db migrate -m "add password_hash"
     flask --app wsgi.py db upgrade
     ```

3. **New auth endpoints** (no API protection required yet):

   * `POST /auth/register` → create user with password
   * `POST /auth/login` → sets **HttpOnly** `access_token_cookie` and returns `{ access_token, user }`
   * `GET /auth/me` → returns current user (requires JWT)
   * `POST /auth/logout` → clears cookie (requires JWT)

4. **Using auth (CLI & Browser)**

   * Start server

     ```bash
     source .venv/bin/activate
     python wsgi.py
     ```
   * **CLI (cookie-based)**

     ```bash
     # register
     curl -X POST http://localhost:8000/auth/register \
       -H "Content-Type: application/json" \
       -d '{"email":"dev@me.com","display_name":"Dev","password":"secret123"}'

     # login and save cookie
     curl -i -c cookies.txt -X POST http://localhost:8000/auth/login \
       -H "Content-Type: application/json" \
       -d '{"email":"dev@me.com","password":"secret123"}'

     # authenticated call
     curl -b cookies.txt http://localhost:8000/auth/me
     ```
   * **Browser (store cookie)** — open DevTools → Console:

     ```js
     await fetch('http://localhost:8000/auth/login', {
       method: 'POST',
       headers: {'Content-Type': 'application/json'},
       body: JSON.stringify({ email: 'dev@me.com', password: 'secret123' }),
       credentials: 'include' // IMPORTANT: save/send HttpOnly cookie
     });
     // Then visit: http://localhost:8000/auth/me
     ```
   * **Bearer token (optional CLI alternative)**

     ```bash
     TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
       -H 'Content-Type: application/json' \
       -d '{"email":"dev@me.com","password":"secret123"}' \
       | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

     curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/auth/me
     ```

5. **CORS for dev (React/Vite, etc.)**
   Allow dev origins and include `/auth/*`:

   ```python
   from flask_cors import CORS
   CORS(app, resources={
     r"/api/*":  {"origins": ["http://localhost:3000","http://localhost:5173","http://localhost:8000"]},
     r"/auth/*": {"origins": ["http://localhost:3000","http://localhost:5173","http://localhost:8000"]},
   }, supports_credentials=True)
   ```

   Frontend `fetch` must use `credentials: 'include'`.

6. **Troubleshooting (auth)**

   * **“Subject must be a string”** → make subject a string on login, cast to int when reading:

     ```python
     # /auth/login
     access_token = create_access_token(identity=str(u.id))
     # /auth/me (and elsewhere)
     uid = int(get_jwt_identity())
     ```
   * **“Missing cookie 'access\_token\_cookie'” in browser** → log in from the browser with `credentials:'include'`.
   * **Token expired (401)** → log in again, or set a dev expiry:

     ```python
     from datetime import timedelta
     app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=3)
     ```
   * **Prod**: enable `JWT_COOKIE_SECURE=True` and `JWT_COOKIE_CSRF_PROTECT=True` (requires HTTPS).

---

## Configuration

Copy `.env.example` to `.env` and customize as needed:

```
FLASK_ENV=development
SECRET_KEY=change-me
# DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/questboard  # For production use
```

By default, the application uses SQLite at `instance/app.db` (the `instance/` directory is automatically created and ignored by Git).

## Development Workflow

* If models are modified:

  ```bash
  flask --app wsgi.py db migrate -m "describe change"
  flask --app wsgi.py db upgrade
  ```
* For a new installation or an empty database:

  ```bash
  flask --app wsgi.py db upgrade
  ```
* If no schema changes are required, simply run:

  ```bash
  python wsgi.py
  ```

## Troubleshooting

* If encountering an "application context" error, ensure `--app wsgi.py` is included in Flask database commands.
* If a migration file is empty, verify that models are imported correctly in the application (via `app/__init__.py`).
* If SQLite reports a locked database, stop the server, execute migrations, and restart.
* For quoting issues on Windows, consider using Postman, Insomnia, or a WSL terminal.

## Project Structure

```
questboard/
├─ app/
│  ├─ __init__.py          # Application factory (initializes database, migrations, registers routes and API)
│  ├─ routes.py            # Handles root ("/") and health ("/health") endpoints
│  ├─ api.py               # Manages /api/* endpoints
│  ├─ auth.py              # Manages /auth/* endpoints (M2)
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

```
```
