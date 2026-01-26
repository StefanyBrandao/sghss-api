from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app import models, schemas

router = APIRouter(prefix="/professionals", tags=["Professionals"])

@router.post("/", response_model=schemas.ProfessionalOut)
def create_professional(payload: schemas.ProfessionalCreate, db: Session = Depends(get_db)):
    # 1) usuário existe
    user = db.query(models.User).filter(models.User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # 2) já existe profissional para o usuário
    exists = db.query(models.Professional).filter(models.Professional.user_id == payload.user_id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Profissional já cadastrado para este usuário")

    professional = models.Professional(
        user_id=payload.user_id,
        registro=payload.registro,
        especialidade=payload.especialidade,
        ativo=True if payload.ativo is None else payload.ativo,
    )
    db.add(professional)
    db.commit()
    db.refresh(professional)
    return professional

@router.get("/", response_model=list[schemas.ProfessionalOut])
def list_professionals(db: Session = Depends(get_db)):
    return db.query(models.Professional).all()

@router.get("/{professional_id}", response_model=schemas.ProfessionalOut)
def get_professional(professional_id: int, db: Session = Depends(get_db)):
    professional = db.query(models.Professional).filter(models.Professional.id == professional_id).first()
    if not professional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    return professional

@router.put("/{professional_id}", response_model=schemas.ProfessionalOut)
def update_professional(professional_id: int, payload: schemas.ProfessionalUpdate, db: Session = Depends(get_db)):
    professional = db.query(models.Professional).filter(models.Professional.id == professional_id).first()
    if not professional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    if payload.registro is not None:
        professional.registro = payload.registro
    if payload.especialidade is not None:
        professional.especialidade = payload.especialidade
    if payload.ativo is not None:
        professional.ativo = payload.ativo

    db.commit()
    db.refresh(professional)
    return professional
