from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import secrets

from app.db import get_db
from app import models, schemas

router = APIRouter(prefix="/teleconsults", tags=["Telemedicine"])

def _fake_meeting_url() -> str:
    # gera um "link"
    token = secrets.token_urlsafe(16)
    return f"https://telemed.local/room/{token}"

@router.post("/", response_model=schemas.TeleconsultOut)
def create_teleconsult(payload: schemas.TeleconsultCreate, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == payload.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    prof = db.query(models.Professional).filter(models.Professional.id == payload.professional_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    if payload.appointment_id is not None:
        appt = db.query(models.Appointment).filter(models.Appointment.id == payload.appointment_id).first()
        if not appt:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    t = models.Teleconsult(
        appointment_id=payload.appointment_id,
        patient_id=payload.patient_id,
        professional_id=payload.professional_id,
        scheduled_at=payload.scheduled_at,
        status="AGENDADA",
        meeting_url=_fake_meeting_url(),
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

@router.get("/patient/{patient_id}", response_model=list[schemas.TeleconsultOut])
def list_patient_teleconsults(patient_id: int, db: Session = Depends(get_db)):
    return db.query(models.Teleconsult).filter(models.Teleconsult.patient_id == patient_id).all()
