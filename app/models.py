from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="PROFISSIONAL")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    profissional = relationship("Professional", back_populates="user", uselist=False)

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False, index=True)
    data_nascimento = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True, index=True)
    telefone = Column(String, nullable=True)
    endereco = Column(String, nullable=True)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    consultas = relationship("Appointment", back_populates="paciente")

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    data_hora = Column(String, nullable=False)
    status = Column(String, nullable=False, default="AGENDADA")
    motivo = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    paciente = relationship("Patient", back_populates="consultas")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    acao = Column(String, nullable=False)
    entidade = Column(String, nullable=False)
    entidade_id = Column(Integer, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    ip = Column(String, nullable=True)

class Professional(Base):
    __tablename__ = "professionals"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    registro = Column(String, nullable=False)          # registro do profissional como CRM/COREN/CRF etc.
    especialidade = Column(String, nullable=True)      # clínica geral, enfermagem...
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="profissional")
