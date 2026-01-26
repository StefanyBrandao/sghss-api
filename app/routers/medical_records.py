from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app import models, schemas

router = APIRouter(prefix="/medical-records", tags=["Medical Records"])

@router.post("/", response_model=schemas.MedicalRecordOut)
def create_record(payload: schemas.MedicalRecordCreate, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == payload.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    if payload.professional_id is not None:
        prof = db.query(models.Professional).filter(models.Professional.id == payload.professional_id).first()
        if not prof:
            raise HTTPException(status_code=404, detail="Profissional não encontrado")

    rec = models.MedicalRecord(
        patient_id=payload.patient_id,
        professional_id=payload.professional_id,
        descricao=payload.descricao,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

@router.get("/patient/{patient_id}", response_model=list[schemas.MedicalRecordOut])
def list_records(patient_id: int, db: Session = Depends(get_db)):
    return db.query(models.MedicalRecord).filter(models.MedicalRecord.patient_id == patient_id).all()
