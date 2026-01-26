from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app import models, schemas

router = APIRouter(prefix="/beds", tags=["Hospital Admin"])

@router.post("/", response_model=schemas.BedOut)
def create_bed(payload: schemas.BedCreate, db: Session = Depends(get_db)):
    exists = db.query(models.Bed).filter(models.Bed.codigo == payload.codigo).first()
    if exists:
        raise HTTPException(status_code=409, detail="Leito já cadastrado")

    bed = models.Bed(codigo=payload.codigo, setor=payload.setor, disponivel=True)
    db.add(bed)
    db.commit()
    db.refresh(bed)
    return bed

@router.get("/", response_model=list[schemas.BedOut])
def list_beds(db: Session = Depends(get_db)):
    return db.query(models.Bed).all()
