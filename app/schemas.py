"""Pydantic Models for Request and Response
"""

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
    
class InteractionResponse(InteractionCreate):
    doctor: DoctorCreate
     
class PatientResponse(PatientCreate):
    id: int
    interactions: List[InteractionResponse] = []

