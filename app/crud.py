"""CRUD Operations"""

import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from . import models, schemas

log = logging.getLogger(__name__)


def get_doctor(db: Session, doctor_id: int):
    """Search doctor_id in database and return relevant data"""

    try:
        return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    except SQLAlchemyError as e:
        log.error(f"Database error: {e}")
        return None


def get_patient(db: Session, patient_id: int):
    """Search patient_id in database and return relevant data"""

    try:
        return db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    except SQLAlchemyError as e:
        log.error(f"Database error: {e}")
        return None


def get_patients(db: Session, skip: int = 0, limit: int = 10):
    """Fetch patients as per filters and return relevant data"""

    try:
        return db.query(models.Patient).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        log.error(f"Database error: {e}")
        return []


def create_interaction(
    db: Session, patient_id: int, interaction: schemas.InteractionCreate
):
    """Create new entry in db as per interaction"""

    try:
        db_interaction = models.Interaction(
            patient_id=patient_id,
            doctor_id=interaction.doctor_id,
            datetime=interaction.datetime,
            notes=interaction.notes,
            healthy=interaction.healthy,
        )
        db.add(db_interaction)
        db.commit()
        db.refresh(db_interaction)
        return db_interaction
    except SQLAlchemyError as e:
        log.error(f"Database error: {e}")
        return None
