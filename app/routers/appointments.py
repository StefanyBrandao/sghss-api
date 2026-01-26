from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.db import get_db
from app import models, schemas


router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=schemas.AppointmentOut)
def create_appointment(payload: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    # validações básicas
    patient = db.query(models.Patient).filter(models.Patient.id == payload.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    prof = db.query(models.Professional).filter(models.Professional.id == payload.professional_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    # impede duplicar horário para o mesmo profissional
    conflict = db.query(models.Appointment).filter(
        and_(
            models.Appointment.professional_id == payload.professional_id,
            models.Appointment.scheduled_at == payload.scheduled_at,
            models.Appointment.status == "AGENDADO",
        )
    ).first()
    if conflict:
        raise HTTPException(status_code=400, detail="Horário indisponível para este profissional")

    appt = models.Appointment(
        patient_id=payload.patient_id,
        professional_id=payload.professional_id,
        scheduled_at=payload.scheduled_at,
        tipo=payload.tipo,
        status="AGENDADO",
    )
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt

@router.post("/{appointment_id}/cancel", response_model=schemas.AppointmentOut)
def cancel_appointment(appointment_id: int, payload: schemas.AppointmentCancel, db: Session = Depends(get_db)):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    appt.status = "CANCELADO"
    db.commit()
    db.refresh(appt)
    return appt

@router.get("/", response_model=list[schemas.AppointmentOut])
def list_appointments(db: Session = Depends(get_db)):
    return db.query(models.Appointment).all()

@router.get("/patient/{patient_id}", response_model=list[schemas.AppointmentOut])
def list_patient_appointments(patient_id: int, db: Session = Depends(get_db)):
    return db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id).all()
