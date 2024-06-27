from datetime import datetime
from typing import List
from pydantic import BaseModel

class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    
class DoctorCreate(BaseModel):
    name: str
    gender: str
    specialty: str

class InteractionCreate(BaseModel):
    doctor_id: int
    datetime: datetime
    notes: str
    healthy: bool

class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    interactions: List[InteractionCreate] = []
    
class InteractionResponse(BaseModel):
    patient_id: int
    doctor_id: int
    datetime: datetime
    notes: str
    healthy: bool