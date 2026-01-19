from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Patient
from ..schemas import PatientCreate, PatientOut, mask_cpf
from ..audit import log_action

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("", response_model=PatientOut)
def create_patient(data: PatientCreate, request: Request, db: Session = Depends(get_db)):
    if db.query(Patient).filter(Patient.cpf == data.cpf).first():
        raise HTTPException(status_code=409, detail="CPF já cadastrado")
    p = Patient(**data.model_dump())
    db.add(p); db.commit(); db.refresh(p)

    # LGPD: não logar CPF inteiro
    log_action(db, user_id=1, acao="CREATE_PATIENT", entidade="patients", entidade_id=p.id,
               ip=request.client.host if request.client else None)

    return PatientOut(
        id=p.id, nome=p.nome, cpf_mascarado=mask_cpf(p.cpf),
        data_nascimento=p.data_nascimento, telefone=p.telefone, endereco=p.endereco, ativo=p.ativo
    )

@router.get("", response_model=list[PatientOut])
def list_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).filter(Patient.ativo == True).all()
    return [
        PatientOut(
            id=p.id, nome=p.nome, cpf_mascarado=mask_cpf(p.cpf),
            data_nascimento=p.data_nascimento, telefone=p.telefone, endereco=p.endereco, ativo=p.ativo
        ) for p in patients
    ]
