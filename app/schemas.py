from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

def mask_cpf(cpf: str) -> str:
    # 12345678900 -> ***.***.***-00 (simples)
    if not cpf or len(cpf) < 2:
        return "***"
    return "***.***.***-" + cpf[-2:]

class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class TokenOut(BaseModel):
    token: str

class PatientCreate(BaseModel):
    nome: str
    cpf: str
    data_nascimento: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None

class PatientOut(BaseModel):
    id: int
    nome: str
    cpf_mascarado: str
    data_nascimento: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    ativo: bool

class AppointmentCreate(BaseModel):
    patient_id: int
    data_hora: str
    motivo: Optional[str] = None

class AppointmentOut(BaseModel):
    id: int
    patient_id: int
    data_hora: str
    status: str
    motivo: Optional[str] = None

class ProfessionalCreate(BaseModel):
    user_id: int
    registro: str
    especialidade: Optional[str] = None
    ativo: Optional[bool] = True

class ProfessionalOut(BaseModel):
    id: int
    user_id: int
    registro: str
    especialidade: Optional[str] = None
    ativo: bool
    created_at: datetime

    class Config:
        from_attributes = True

