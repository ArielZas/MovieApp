# Movie Library API

A RESTful API for managing a personal movie library, built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

Features user registration, JWT authentication, full CRUD for movies, and a personal watchlist.

---

## Getting started

**Prerequisites:** Python 3.10+

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

The server starts at `http://127.0.0.1:8000`.

Interactive docs are available at:
- `/docs` — Swagger UI (try every endpoint here)
- `/redoc` — read-only reference

The database file `movieapp.db` is created automatically on first run. To reset all data, delete it and restart the server.

---

## Running tests

```bash
pytest tests.py -v
```

Tests use an in-memory SQLite database and are fully isolated from the development database.

---

## Endpoints

### Authentication

All movie endpoints require a Bearer token. To get one:

1. Register — `POST /users/register`
2. Login — `POST /users/login` — returns a JWT access token
3. Pass the token in the `Authorization: Bearer <token>` header

### Movies

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| GET | `/movies/` | Yes | List all movies |
| GET | `/movies/{id}` | Yes | Get a movie by ID |
| POST | `/movies/` | Admin | Create a movie |
| PUT | `/movies/{id}` | Admin | Update a movie |
| DELETE | `/movies/{id}` | Admin | Delete a movie |

### Users

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| POST | `/users/register` | No | Create an account |
| POST | `/users/login` | No | Get a JWT token |
| GET | `/users/me` | Yes | Get your profile |
| DELETE | `/users/` | Yes | Delete your account |

### Watchlist

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| GET | `/watchlist/` | Yes | List your watchlist |
| POST | `/watchlist/` | Yes | Add a movie |
| PUT | `/watchlist/{movie_id}` | Yes | Mark watched / update |
| DELETE | `/watchlist/{movie_id}` | Yes | Remove a movie |
| GET | `/watchlist/unwatched` | Yes | List unwatched items |

---

## Project structure

```
MovieApp/
├── main.py
├── database.py
│
├── movies/
│   ├── models.py       # ORM model
│   ├── schemes.py      # Pydantic schemas
│   ├── storage.py      # Database queries
│   ├── services.py     # Business logic
│   └── router.py       # Route handlers
│
├── users/
│   ├── models.py
│   ├── schemes.py
│   ├── auth.py         # Password hashing + JWT
│   ├── storage.py
│   ├── services.py
│   ├── dependencies.py # get_current_user dependency
│   └── router.py
│
├── watchlist/
│   ├── models.py
│   ├── schemes.py
│   ├── storage.py
│   ├── services.py
│   └── router.py
│
├── config.py
├── tests.py
└── requirements.txt
```

Each layer has a single responsibility. Swapping databases (e.g. to PostgreSQL) only requires changing `DATABASE_URL` in `database.py`.
