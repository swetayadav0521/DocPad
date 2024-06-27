from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    
class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    gender = Column(String)
    specialty = Column(String)

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    datetime = Column(DateTime, default=datetime.now()) # Column(Date)
    notes = Column(String)
    healthy = Column(Boolean)
    patient = relationship("Patient", back_populates="interactions")
    doctor = relationship("Doctor", back_populates="interactions")

Patient.interactions = relationship("Interaction", order_by=Interaction.id, back_populates="patient")
Doctor.interactions = relationship("Interaction", order_by=Interaction.id, back_populates="doctor")