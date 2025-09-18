# Questboard (MQ)

Minimal Flask skeleton.

## Quickstart

1. Create a virtualenv

   ```bash
   python -m venv venv
   ```

   # Windows: venv\Scripts\activate

   # Linux/Mac: source venv/bin/activate

2. Install deps

   ```bash
   pip install -r requirements.txt
   ```

3. Env vars

   ```bash
   cp env.example .env
   ```

4. Run dev server

   ```bash
   python wsgi.py
   ```

5. Test endpoints

   * http://localhost:8000/health -> `{"status": "ok"}`

   * http://localhost:8000/ -> `{"app": "Questboard", "message": "Welcome!"}`