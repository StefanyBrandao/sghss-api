from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app import models, schemas
from app.audit import log_action

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=schemas.PatientPublicOut)
def create_patient(data: schemas.PatientCreate, request: Request, db: Session = Depends(get_db)):
    if db.query(models.Patient).filter(models.Patient.cpf == data.cpf).first():
        raise HTTPException(status_code=409, detail="CPF já cadastrado")
    if db.query(models.Patient).filter(models.Patient.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email já cadastrado")

    p = models.Patient(**data.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)

    # LGPD: não logar CPF inteiro
    log_action(
        db,
        user_id=None,
        acao="CREATE_PATIENT",
        entidade="patients",
        entidade_id=p.id,
        ip=request.client.host if request.client else None,
    )

    return schemas.PatientPublicOut(
        id=p.id,
        nome=p.nome,
        email=p.email,
        cpf_masked=schemas.mask_cpf(p.cpf),
        telefone=p.telefone,
        created_at=p.created_at,
    )

@router.get("/", response_model=list[schemas.PatientPublicOut])
def list_patients(db: Session = Depends(get_db)):
    patients = db.query(models.Patient).all()
    return [
        schemas.PatientPublicOut(
            id=p.id,
            nome=p.nome,
            email=p.email,
            cpf_masked=schemas.mask_cpf(p.cpf),
            telefone=p.telefone,
            created_at=p.created_at,
        )
        for p in patients
    ]

@router.get("/{patient_id}", response_model=schemas.PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    p = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return p
