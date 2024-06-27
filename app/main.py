# app/main.py

from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# @app.post("/interactions")
# def record_interaction(interaction: schemas.InteractionCreate, db: Session = Depends(get_db)):
#     """API to record interactions between doctor and patient"""
#     db_patient = crud.get_patient(db, patient_id=interaction.patient_id)
#     db_doctor = crud.get_doctor(db, doctor_id=interaction.doctor_id)
#     if (db_patient or db_doctor) is None:
#         raise HTTPException(status_code=404, detail="Patient not found")
#     return crud.create_interaction(db=db, interaction=interaction)

@app.post("/patient/{patient_id}/interactions", response_model=schemas.InteractionResponse)
def record_interaction(patient_id: int, interaction: schemas.InteractionCreate, db: Session = Depends(get_db)):
    """API to record interactions between doctor and patient"""
    db_patient = crud.get_patient(db, patient_id=patient_id)
    db_doctor = crud.get_doctor(db, doctor_id=interaction.doctor_id)
    if (db_patient or db_doctor) is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return crud.create_interaction(db=db, patient_id=patient_id, interaction=interaction)

@app.get("/patient/{patient_id}", response_model=schemas.PatientResponse)
def get_patient_history(patient_id: int, db: Session = Depends(get_db)):
    """API to get particular patient history"""
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail=f"Patient not found, id:{patient_id!r}")
    return db_patient

@app.get("/patients", response_model=List[schemas.PatientResponse])
def get_patients_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """API to get all patients history"""
    return crud.get_patients(db, skip=skip, limit=limit)
