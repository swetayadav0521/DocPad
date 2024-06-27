# init_db.py

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
    patient1 = models.Patient(name="John Doe", age=30, gender="Male")
    patient2 = models.Patient(name="Jane Smith", age=25, gender="Male")
    logger.info("Added Patient2: %s", patient2.name)

    db.add(patient1)
    db.add(patient2)
    db.commit()

    # Create initial doctor
    doctor = models.Doctor(
        name="Dr. Baymax", gender="Male", specialty="General Practice"
    )

    db.add(doctor)
    db.commit()

    # Create initial interactions
    interaction1 = models.Interaction(
        patient_id=patient1.id,
        doctor_id=doctor.id,
        notes="Annual checkup",
        healthy=True,
    )
    interaction2 = models.Interaction(
        patient_id=patient1.id,
        doctor_id=doctor.id,
        notes="Follow-up visit",
        healthy=True,
    )
    interaction3 = models.Interaction(
        patient_id=patient2.id,
        doctor_id=doctor.id,
        notes="Initial consultation",
        healthy=False,
    )

    db.add(interaction1)
    db.add(interaction2)
    db.add(interaction3)
    db.commit()

    db.close()


if __name__ == "__main__":
    init_db()
