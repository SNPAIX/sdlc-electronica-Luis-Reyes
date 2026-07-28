import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db import Base, get_db

# Base de datos SQLite en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "SensorHub IoT API"}

def test_create_reading_success():
    payload = {
        "sensor_id": "TEST-SENSOR-1",
        "temperature": 22.5,
        "humidity": 45.0
    }
    response = client.post("/readings/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["sensor_id"] == "TEST-SENSOR-1"
    assert data["is_anomaly"] is False

def test_create_reading_physical_validation_error():
    # Humedad fuera del rango real (> 100%)
    payload = {
        "sensor_id": "TEST-SENSOR-1",
        "temperature": 22.5,
        "humidity": 150.0
    }
    response = client.post("/readings/", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

def test_list_readings_with_pagination():
    # Ingestar lectura
    client.post("/readings/", json={"sensor_id": "S1", "temperature": 30.0, "humidity": 50.0})
    
    response = client.get("/readings/?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["sensor_id"] == "S1"