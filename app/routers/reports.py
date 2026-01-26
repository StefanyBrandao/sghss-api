from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app import models, schemas

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/summary", response_model=schemas.ReportOut)
def summary(db: Session = Depends(get_db)):
    patients_total = db.query(models.Patient).count()
    professionals_total = db.query(models.Professional).count()
    appointments_total = db.query(models.Appointment).count()
    admissions_active = db.query(models.Admission).filter(models.Admission.status == "INTERNADO").count()

    return schemas.ReportOut(
        patients_total=patients_total,
        professionals_total=professionals_total,
        appointments_total=appointments_total,
        admissions_active=admissions_active,
    )
