# test_main.py

import atexit
from datetime import datetime
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app import models
from app.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
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
    patient_id = setup_db["patient"].id
    doctor_id = setup_db["doctor"].id
    interaction_data = {"patient_id": patient_id, "doctor_id": doctor_id, "notes": "Routine Checkup", "healthy":True, "datetime": str(datetime.now())}
    
    response = client.post(f"/patient/{patient_id}/interactions", json=interaction_data)

    assert response.status_code == 200
    assert response.json()["patient_id"] == patient_id
    assert response.json()["doctor_id"] == doctor_id
    assert response.json()["healthy"]

def test_read_patient(setup_db):
    patient_id = setup_db["patient"].id
    
    response = client.get(f"/patient/{patient_id}")
    assert response.status_code == 200
    assert response.json()["id"] == patient_id
    assert response.json()["name"] == setup_db["patient"].name

def test_read_patients(setup_db):
    response = client.get("/patients")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["name"] == setup_db["patient"].name


# Cleanup function to remove the test database file after tests
def cleanup_test_db():
    if os.path.exists("./test.db"):
        os.remove("./test.db")

# Register the cleanup function to be called upon exit
atexit.register(cleanup_test_db)