"""Script to initialize database with dummy data"""

import csv
import logging
import os
from sqlalchemy import create_engine
from app import models

# from app.database import engine, SessionLocal
from sqlalchemy.orm import sessionmaker


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database and the tables
models.Base.metadata.create_all(bind=engine)


def init_db():
    db = SessionLocal()

    # Create initial patients
    with open("dummy_data/patients.csv", "r") as csvfile:
        # creating a csv dict reader object for patients
        records = csv.DictReader(csvfile)

        for record in records:
            patient = models.Patient(
                name=record["name"], age=record["age"], gender=record["gender"]
            )
            db.add(patient)
            db.commit()

    # Create initial doctor
    with open("dummy_data/doctors.csv", "r") as csvfile:
        # creating a csv dict reader object for doctors
        records = csv.DictReader(csvfile)

        for record in records:
            doctor = models.Doctor(
                name=record["name"],
                gender=record["gender"],
                specialty=record["specialty"],
            )
            db.add(doctor)
            db.commit()

    # Create initial interactions
    interaction_notes = [
        {"notes": "Annual checkup"},
        {"notes": "Follow-up visit"},
        {"notes": "Initial consultation"},
    ]
    for id in range(1, 11):
        for notes in interaction_notes:
            interaction = models.Interaction(
                patient_id=id,
                doctor_id=id,
                notes=notes["notes"],
                healthy=True,
            )
            db.add(interaction)
            db.commit()

    db.close()


if __name__ == "__main__":
    init_db()
