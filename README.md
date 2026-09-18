# BudgetBite

A Python budgeting app built with Flask, so the frontend (Jinja2 templates)
and backend (Python routes) run together in one server — no separate
frontend/backend processes needed while you're building and testing.

## Project structure

```
budgetbite/
│
├── run.py                 # Entry point — run this to start the server
├── config.py               # App configuration (secret key, database URI)
├── requirements.txt         # Python dependencies
│
├── app/                     # Backend application package
│   ├── __init__.py          # App factory: creates and configures the Flask app
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # User table (username, email, hashed password)
│   └── routes/
│       ├── __init__.py
│       ├── auth.py          # /login, /register, /logout
│       └── main.py          # /, /dashboard
│
├── templates/                # Frontend HTML (Jinja2)
│   ├── base.html             # Shared layout + flash messages
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
│
├── static/
│   ├── css/style.css
│   ├── js/                   # empty for now — add JS here as you need it
│   └── img/
│
└── instance/
    └── budgetbite.db          # SQLite database (auto-created on first run)
```

## Why this structure

- **`app/` uses the "application factory" pattern** (`create_app()`), which
  is the standard way to structure a Flask project once it grows past a
  single file. It keeps routes, models, and config separate so the project
  doesn't turn into one giant `app.py`.
- **Blueprints** (`auth.py`, `main.py`) group related routes together.
  Later, when you add a `budget` blueprint (for tracking expenses), it
  drops in next to `auth` the same way.
- **`templates/` and `static/`** are Flask's default folders for
  frontend files — Flask finds them automatically.

## Running it

```bash
cd budgetbite
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Then open `http://127.0.0.1:5000` in your browser. It'll redirect you to
`/login` since there's no logged-in user yet. Click "Sign up" to create
an account, then log in — you'll land on `/dashboard`.

## How the login actually works

1. `register.html` posts to `auth.register`, which hashes the password
   with `werkzeug.security.generate_password_hash` and saves a `User` row.
   **Passwords are never stored in plain text.**
2. `login.html` posts to `auth.login`, which looks up the user by
   username and calls `user.check_password()` to verify.
3. On success, `flask_login.login_user()` stores the user's session —
   this is what lets `@login_required` protect `/dashboard`.
4. `logout` clears that session.

## Testing frontend + backend together

Because Flask renders the HTML server-side, every change you make to a
route (`auth.py`) or a template (`login.html`) shows up on refresh — with
`debug=True` in `run.py`, the server even auto-reloads. So your workflow is:
edit → save → refresh browser → repeat, on both sides at once.
