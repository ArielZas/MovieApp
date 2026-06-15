# Movie Library API

A RESTful API built with **FastAPI + SQLAlchemy (SQLite)** for managing a personal movie library.
Supports user registration, JWT authentication, full CRUD for movies, and a personal watchlist.

---

## Quickstart

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open:
- **http://127.0.0.1:8000/docs** — interactive Swagger UI (try every endpoint here)
- **http://127.0.0.1:8000/redoc** — clean read-only docs

Run tests:
```bash
pytest tests.py -v
```

The database file `movieapp.db` is created automatically on first run.
To reset all data, delete it and restart the server.

---

## Project structure

```
MovieApp/
├── main.py                  # App entry point — creates DB tables, registers routers
├── database.py              # SQLAlchemy engine, SessionLocal, Base, get_db()
│
├── movies/
│   ├── models.py            # SQLAlchemy ORM model → "movies" table
│   ├── schemes.py           # Pydantic schemas (MovieCreate, MovieResponse, …)
│   ├── storage.py           # Data layer — SQLAlchemy CRUD queries
│   ├── services.py          # Business logic — converts ORM objects → Pydantic
│   └── router.py            # HTTP layer — URL routes & status codes
│
├── users/
│   ├── models.py            # SQLAlchemy ORM model → "users" table
│   ├── schemes.py           # Pydantic schemas (UserCreate, Token, …)
│   ├── auth.py              # bcrypt password hashing + JWT helpers
│   ├── storage.py           # Data layer — user lookup & creation
│   ├── dependencies.py      # FastAPI dependency injection (get_current_user)
│   └── router.py            # HTTP layer — register, login, /me
│
├── watchlist/               # ← YOUR TODO (see below)
│   ├── models.py            # SQLAlchemy ORM model → "watchlist" table (done)
│   ├── schemes.py           # Pydantic schemas (done)
│   ├── storage.py           # Data layer — ALL TODO
│   ├── services.py          # Business logic — ALL TODO
│   └── router.py            # HTTP layer — ALL TODO (routes commented out)
│
├── tests.py                 # Integration tests (pytest + TestClient + test DB)
└── requirements.txt
```

### Layer architecture

```
Client  →  Router (HTTP)  →  Service (logic)  →  Storage (SQLAlchemy)  →  SQLite DB
        ←  JSON response  ←  Pydantic schema  ←  ORM model             ←
```

Each layer has one job. Swapping the database (e.g. to PostgreSQL) means only
changing the `DATABASE_URL` in `database.py` — every other layer stays the same.

---

## Implemented endpoints

### Movies
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/movies/` | List all movies |
| POST | `/movies/` | Create a movie |
| GET | `/movies/{id}` | Get one movie |
| PUT | `/movies/{id}` | Update a movie (partial) |
| DELETE | `/movies/{id}` | Delete a movie |

### Users
| Method | URL | Auth required |
|--------|-----|---------------|
| POST | `/users/register` | No |
| POST | `/users/login` | No — returns a JWT token |
| GET | `/users/me` | Yes — Bearer token |

---

## TODO exercises

Work through the layers in order: **storage → service → router → tests**.

### 1. Movies — filter / search (storage + service + router)

Implement these in [movies/storage.py](movies/storage.py), then the matching wrappers
in [movies/services.py](movies/services.py), then uncomment the routes in
[movies/router.py](movies/router.py).

| Storage function | SQL equivalent |
|---|---|
| `get_movies_by_genre(db, genre)` | `WHERE genre = :genre` |
| `search_movies_by_title(db, query)` | `WHERE title ILIKE '%query%'` |
| `get_top_rated_movies(db, limit)` | `WHERE rating IS NOT NULL ORDER BY rating DESC LIMIT n` |
| `get_movies_by_year_range(db, start, end)` | `WHERE year BETWEEN :start AND :end` |
| `get_movies_by_director(db, director)` | `WHERE director ILIKE '%director%'` |

Once storage is done, wire each one up through the service and uncomment the
matching router TODO (routes: `/genre/{genre}`, `/search`, `/top-rated`, `/year-range`).

### 2. Users — extra endpoints

| Location | What to implement |
|---|---|
| `users/storage.py` | `get_all_users(db)` and `delete_user(db, user_id)` |
| `users/dependencies.py` | `get_current_user_optional()` — returns user or None instead of 401 |
| `users/router.py` | `GET /users/{user_id}` (public) and `POST /users/change-password` (protected) |

### 3. Watchlist — your main TODO

The DB table and Pydantic schemas are already written for you in
[watchlist/models.py](watchlist/models.py) and [watchlist/schemes.py](watchlist/schemes.py).
Your job is to implement the three remaining files, then wire up the router in `main.py`.

**Step 1 — [watchlist/storage.py](watchlist/storage.py)**

| Function | What it does |
|---|---|
| `get_watchlist_for_user(db, user_id)` | All items for a user |
| `get_watchlist_item(db, user_id, movie_id)` | One item by user + movie |
| `add_to_watchlist(db, user_id, item_data)` | Insert; return None if duplicate |
| `update_watchlist_item(db, user_id, movie_id, item_update)` | Mark watched etc. |
| `remove_from_watchlist(db, user_id, movie_id)` | Delete; return bool |
| `get_unwatched_for_user(db, user_id)` | Items where `watched == False` |

**Step 2 — [watchlist/services.py](watchlist/services.py)**

Thin wrappers that call the storage functions and convert
`WatchlistItem` ORM objects → `WatchlistItemResponse` Pydantic schemas.

**Step 3 — [watchlist/router.py](watchlist/router.py)**

Uncomment the 5 routes one by one and test each in `/docs`:

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/watchlist/` | List my watchlist |
| POST | `/watchlist/` | Add a movie to my watchlist |
| PUT | `/watchlist/{movie_id}` | Mark watched / update entry |
| DELETE | `/watchlist/{movie_id}` | Remove from watchlist |
| GET | `/watchlist/unwatched` | Only unwatched items |

**Step 4 — wire it up in `main.py`**

Uncomment `from watchlist.router import router as watchlist_router` and
`app.include_router(watchlist_router)`.

**Step 5 — write the tests**

Add watchlist tests to `tests.py` following the same pattern as the movie/user tests.
The `reset_db` fixture already handles clearing the database between tests.

### 4. Test stubs (fill in the `pass` bodies)

| Test | What to assert |
|---|---|
| `test_get_movies_by_genre` | Only the matching genre is returned |
| `test_search_movies_by_title` | Partial case-insensitive title match works |
| `test_top_rated_movies` | Results are sorted highest rating first |
