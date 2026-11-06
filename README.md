# Cat Registration (test project)

Flask + plain JS + PostgreSQL. Registrations are stored in `cat.family`.

## Run locally

```bash
cd "Test Project Cat"

# 1. Database + table
createdb catdb
psql catdb -f schema.sql

# 2. Python env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Config
cp .env.example .env      # edit DATABASE_URL with your user/password

# 4. Start
python app.py             # http://localhost:5000
```

## API

| Method | Path        | Body / result                                        |
|--------|-------------|------------------------------------------------------|
| GET    | `/api/cats` | list of all cats, newest first                       |
| POST   | `/api/cats` | JSON `{name, breed, age, gender, color, owner_name, owner_phone}`; `name` and `owner_name` required |

## Deploy (free): Render + Neon

1. Neon: create a project, run `schema.sql` in its SQL editor, copy the connection string.
2. Render: New → Web Service → this repo.
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
   - Env var: `DATABASE_URL` = Neon connection string