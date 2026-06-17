import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

# ============================================================
# tests.py  —  INTEGRATION TESTS WITH A REAL (TEST) DATABASE
#
# We use a SEPARATE SQLite file for tests so we never touch
# the production movieapp.db. The reset_db fixture drops and
# recreates all tables before every test, giving each test a
# clean slate.
#
# HOW TO RUN:
#   pip install pytest httpx
#   pytest tests.py -v
# ============================================================

TEST_DATABASE_URL = "sqlite:///./test_movieapp.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Replaces get_db() for the duration of the test suite."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Swap out the real DB dependency with the test one.
# Any route that uses Depends(get_db) now gets a test session instead.
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """
    Drop and recreate all tables before every test.
    autouse=True means every test gets this automatically —
    no need to declare it as a parameter.
    """
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


# ============================================================
# HEALTH CHECK
# ============================================================

def test_root_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ============================================================
# MOVIE CRUD
# ============================================================

SAMPLE_MOVIE = {
    "title": "Inception",
    "year": 2010,
    "genre": "Sci-Fi",
    "duration": 148,
    "director": "Christopher Nolan",
    "description": "A thief who steals corporate secrets through dream-sharing.",
    "rating": 8.8,
}


def test_create_movie():
    response = client.post("/movies/", json=SAMPLE_MOVIE)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Inception"
    assert isinstance(data["id"], int)


def test_list_movies():
    client.post("/movies/", json=SAMPLE_MOVIE)
    client.post("/movies/", json={**SAMPLE_MOVIE, "title": "Interstellar"})
    response = client.get("/movies/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_movie():
    movie_id = client.post("/movies/", json=SAMPLE_MOVIE).json()["id"]
    response = client.get(f"/movies/{movie_id}")
    assert response.status_code == 200
    assert response.json()["id"] == movie_id


def test_get_movie_not_found():
    response = client.get("/movies/99999")
    assert response.status_code == 404


def test_update_movie():
    movie_id = client.post("/movies/", json=SAMPLE_MOVIE).json()["id"]
    response = client.put(f"/movies/{movie_id}", json={"rating": 9.5})
    assert response.status_code == 200
    assert response.json()["rating"] == 9.5
    assert response.json()["title"] == "Inception"   # unchanged


def test_delete_movie():
    movie_id = client.post("/movies/", json=SAMPLE_MOVIE).json()["id"]
    assert client.delete(f"/movies/{movie_id}").status_code == 204
    assert client.get(f"/movies/{movie_id}").status_code == 404


def test_create_movie_invalid_year():
    response = client.post("/movies/", json={**SAMPLE_MOVIE, "year": 1800})
    assert response.status_code == 422   # Pydantic validation error


def test_create_movie_invalid_rating():
    response = client.post("/movies/", json={**SAMPLE_MOVIE, "rating": 15.0})
    assert response.status_code == 422


def test_create_movie_invalid_genre():
    response = client.post("/movies/", json={**SAMPLE_MOVIE, "genre": "NotAGenre"})
    assert response.status_code == 422


# ============================================================
# USER AUTH
# ============================================================

SAMPLE_USER = {"username": "testuser", "password": "password123"}


def test_register_user():
    response = client.post("/users/register", json=SAMPLE_USER)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_username():
    client.post("/users/register", json=SAMPLE_USER)
    response = client.post("/users/register", json=SAMPLE_USER)
    assert response.status_code == 409


def test_login_success():
    client.post("/users/register", json=SAMPLE_USER)
    response = client.post("/users/login", data=SAMPLE_USER)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    client.post("/users/register", json=SAMPLE_USER)
    response = client.post("/users/login", data={**SAMPLE_USER, "password": "wrong"})
    assert response.status_code == 401


def test_login_unknown_user():
    response = client.post("/users/login", data={"username": "nobody", "password": "x"})
    assert response.status_code == 401


def _get_auth_header() -> dict:
    """Helper: register, login, return the Authorization header dict."""
    client.post("/users/register", json=SAMPLE_USER)
    token = client.post("/users/login", data=SAMPLE_USER).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_me():
    headers = _get_auth_header()
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_get_me_no_token():
    assert client.get("/users/me").status_code == 401


def test_get_me_bad_token():
    response = client.get("/users/me", headers={"Authorization": "Bearer garbage"})
    assert response.status_code == 401


# ============================================================
# TODO EXERCISES — fill these in once you implement the
# matching storage / service / router TODO functions.
# ============================================================

def test_get_movies_by_genre():
    """
    TODO: Create a Sci-Fi and a Drama movie.
    GET /movies/genre/Sci-Fi should return only the Sci-Fi one.
    """
    pass


def test_search_movies_by_title():
    """
    TODO: Create a movie called "Inception".
    GET /movies/search?q=incep should find it (partial match).
    """
    pass


def test_top_rated_movies():
    """
    TODO: Create movies with ratings 7.0, 9.0, 8.0.
    GET /movies/top-rated?limit=3 should return them highest-first.
    """
    pass
