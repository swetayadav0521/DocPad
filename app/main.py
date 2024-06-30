"""FastAPI Application"""

import logging
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

log = logging.getLogger(__name__)


@app.post(
    "/patient/{patient_id}/interaction", response_model=schemas.InteractionResponse
)
async def record_interaction(
    patient_id: int,
    interaction: schemas.InteractionCreate,
    db: Session = Depends(get_db),
):
    """API to record interactions between doctor and patient"""

    db_patient = crud.get_patient(db, patient_id=patient_id)
    db_doctor = crud.get_doctor(db, doctor_id=interaction.doctor_id)

    # Check if both patient and doctor exist
    if not db_patient and not db_doctor:
        raise HTTPException(
            status_code=404, 
            detail=f"Unable to find Doctor with id {interaction.doctor_id} and Patient with id {patient_id}"
        )
    
    # Check if the patient exists
    if not db_patient:
        raise HTTPException(
            status_code=404, 
            detail=f"Unable to find Patient with id {patient_id}"
        )
    
    # Check if the doctor exists
    if not db_doctor:
        raise HTTPException(
            status_code=404, 
            detail=f"Unable to find Doctor with id {interaction.doctor_id}"
        )
    return crud.create_interaction(
        db=db, patient_id=patient_id, interaction=interaction
    )


@app.get("/patient/{patient_id}", response_model=schemas.PatientResponse)
async def get_patient_history(patient_id: int, db: Session = Depends(get_db)):
    """API to get particular patient history"""

    db_patient = crud.get_patient(db, patient_id=patient_id)

    if db_patient is None:
        raise HTTPException(
            status_code=404, detail=f"Unable to find Patient id {patient_id!r}"
        )
    return db_patient


@app.get("/patients", response_model=List[schemas.PatientResponse])
async def get_patients_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """API to get all patients history"""

    if (skip or limit) < 0:
        raise HTTPException(status_code=405, detail="Negative values are not allowed")
    return crud.get_patients(db, skip=skip, limit=limit)
