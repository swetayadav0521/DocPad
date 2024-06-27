# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas

def get_doctor(db: Session, doctor_id: int):
    return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def get_patients(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Patient).offset(skip).limit(limit).all()

def create_interaction(db: Session, patient_id: int,  interaction: schemas.InteractionCreate):
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
