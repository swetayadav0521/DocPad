# test_main.py

import atexit
import os
import pytest

from app import models
from datetime import datetime
from sqlalchemy import create_engine

from app.database import Base
from app.main import app, get_db
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def setup_db():
    db = TestingSessionLocal()

    # Create a test patient and doctor
    patient = models.Patient(name="Test Patient", age=23, gender="Male")
    doctor = models.Doctor(name="Test Doctor", gender="Female", specialty="General Practice")
    db.add(patient)
    db.add(doctor)
    db.commit()
    db.refresh(patient)
    db.refresh(doctor)
    yield {"patient": patient, "doctor": doctor}

def test_create_interaction(setup_db):
    # Record doctor and patient interaction endpoint
    patient_id = setup_db["patient"].id
    doctor_id = setup_db["doctor"].id
    interaction_data = {"patient_id": patient_id, "doctor_id": doctor_id, "notes": "Routine Checkup", "healthy":True, "datetime": str(datetime.now())}
    
    response = client.post(f"/patient/{patient_id}/interaction", json=interaction_data)

    assert response.status_code == 200
    assert response.json()["patient_id"] == patient_id
    assert response.json()["doctor_id"] == doctor_id
    assert response.json()["healthy"]

def test_read_patient(setup_db):
    # Read particlur patient endpoint
    patient_id = setup_db["patient"].id
    
    response = client.get(f"/patient/{patient_id}")
    assert response.status_code == 200
    assert response.json()["id"] == patient_id
    assert response.json()["name"] == setup_db["patient"].name

def test_read_patients(setup_db):
    # Read patients endpoint
    response = client.get("/patients")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["name"] == setup_db["patient"].name

def cleanup_test_db():
    # Cleanup function to remove the test database file after tests
    if os.path.exists("./test.db"):
        os.remove("./test.db")

# Register the cleanup function to be called upon exit
atexit.register(cleanup_test_db)