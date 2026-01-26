from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

try:
    from pydantic import ConfigDict  # type: ignore

    class ORMBase(BaseModel):
        model_config = ConfigDict(from_attributes=True)
except Exception:
    class ORMBase(BaseModel):
        class Config:
            orm_mode = True


def mask_cpf(cpf: str) -> str:
    # 12345678900 -> ***.***.***-00 (simples)
    if not cpf or len(cpf) < 2:
        return "***"
    return "***.***.***-" + cpf[-2:]


class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str


class UserOut(ORMBase):
    id: int
    nome: str
    email: EmailStr
    role: str
    created_at: datetime


class TokenOut(BaseModel):
    token: str



class PatientCreate(BaseModel):
    nome: str
    email: EmailStr
    cpf: str
    telefone: Optional[str] = None


class PatientOut(ORMBase):
    id: int
    nome: str
    email: EmailStr
    cpf: str
    telefone: Optional[str] = None
    created_at: datetime


class PatientPublicOut(ORMBase):
    id: int
    nome: str
    email: EmailStr
    cpf_masked: str
    telefone: Optional[str] = None
    created_at: datetime



class ProfessionalCreate(BaseModel):
    user_id: int
    registro: str
    especialidade: Optional[str] = None
    ativo: Optional[bool] = True


class ProfessionalUpdate(BaseModel):
    registro: Optional[str] = None
    especialidade: Optional[str] = None
    ativo: Optional[bool] = None


class ProfessionalOut(ORMBase):
    id: int
    user_id: int
    registro: str
    especialidade: Optional[str] = None
    ativo: bool
    created_at: datetime


# --- Appointments (agendar/cancelar) ---
class AppointmentCreate(BaseModel):
    patient_id: int
    professional_id: int
    scheduled_at: datetime
    tipo: str = "PRESENCIAL"


class AppointmentOut(ORMBase):
    id: int
    patient_id: int
    professional_id: int
    scheduled_at: datetime
    tipo: str
    status: str
    created_at: datetime


class AppointmentCancel(BaseModel):
    motivo: Optional[str] = None


# --- Prontuário ---
class MedicalRecordCreate(BaseModel):
    patient_id: int
    professional_id: Optional[int] = None
    descricao: str


class MedicalRecordOut(ORMBase):
    id: int
    patient_id: int
    professional_id: Optional[int] = None
    descricao: str
    created_at: datetime


# --- Receitas ---
class PrescriptionCreate(BaseModel):
    patient_id: int
    professional_id: int
    medicamento: str
    dosagem: Optional[str] = None
    instrucoes: Optional[str] = None


class PrescriptionOut(ORMBase):
    id: int
    patient_id: int
    professional_id: int
    medicamento: str
    dosagem: Optional[str] = None
    instrucoes: Optional[str] = None
    issued_at: datetime


# --- Telemedicina (teleconsulta) ---
class TeleconsultCreate(BaseModel):
    patient_id: int
    professional_id: int
    scheduled_at: datetime
    appointment_id: Optional[int] = None


class TeleconsultOut(ORMBase):
    id: int
    appointment_id: Optional[int] = None
    patient_id: int
    professional_id: int
    scheduled_at: datetime
    status: str
    meeting_url: Optional[str] = None
    created_at: datetime


# --- Leitos / Internações ---
class BedCreate(BaseModel):
    codigo: str
    setor: Optional[str] = None


class BedOut(ORMBase):
    id: int
    codigo: str
    setor: Optional[str] = None
    disponivel: bool


class AdmissionCreate(BaseModel):
    patient_id: int
    bed_id: int


class AdmissionDischarge(BaseModel):
    discharged_at: Optional[datetime] = None


class AdmissionOut(ORMBase):
    id: int
    patient_id: int
    bed_id: int
    status: str
    admitted_at: datetime
    discharged_at: Optional[datetime] = None


# --- Relatórios simples ---
class ReportOut(BaseModel):
    patients_total: int
    professionals_total: int
    appointments_total: int
    admissions_active: int
