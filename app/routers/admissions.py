from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db import get_db
from app import models, schemas

router = APIRouter(prefix="/admissions", tags=["Hospital Admin"])

@router.post("/", response_model=schemas.AdmissionOut)
def admit(payload: schemas.AdmissionCreate, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == payload.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    bed = db.query(models.Bed).filter(models.Bed.id == payload.bed_id).first()
    if not bed:
        raise HTTPException(status_code=404, detail="Leito não encontrado")
    if not bed.disponivel:
        raise HTTPException(status_code=400, detail="Leito indisponível")

    adm = models.Admission(patient_id=payload.patient_id, bed_id=payload.bed_id, status="INTERNADO")
    bed.disponivel = False
    db.add(adm)
    db.commit()
    db.refresh(adm)
    return adm

@router.post("/{admission_id}/discharge", response_model=schemas.AdmissionOut)
def discharge(admission_id: int, payload: schemas.AdmissionDischarge, db: Session = Depends(get_db)):
    adm = db.query(models.Admission).filter(models.Admission.id == admission_id).first()
    if not adm:
        raise HTTPException(status_code=404, detail="Internação não encontrada")

    adm.status = "ALTA"
    adm.discharged_at = payload.discharged_at or datetime.utcnow()

    bed = db.query(models.Bed).filter(models.Bed.id == adm.bed_id).first()
    if bed:
        bed.disponivel = True

    db.commit()
    db.refresh(adm)
    return adm

@router.get("/", response_model=list[schemas.AdmissionOut])
def list_admissions(db: Session = Depends(get_db)):
    return db.query(models.Admission).all()
