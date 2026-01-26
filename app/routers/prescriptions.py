from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app import models, schemas

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])

@router.post("/", response_model=schemas.PrescriptionOut)
def create_prescription(payload: schemas.PrescriptionCreate, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == payload.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    prof = db.query(models.Professional).filter(models.Professional.id == payload.professional_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    p = models.Prescription(
        patient_id=payload.patient_id,
        professional_id=payload.professional_id,
        medicamento=payload.medicamento,
        dosagem=payload.dosagem,
        instrucoes=payload.instrucoes,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.get("/patient/{patient_id}", response_model=list[schemas.PrescriptionOut])
def list_prescriptions(patient_id: int, db: Session = Depends(get_db)):
    return db.query(models.Prescription).filter(models.Prescription.patient_id == patient_id).all()
