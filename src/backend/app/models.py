from datetime import datetime, date
from sqlalchemy import String, Text, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from .database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    clerk_user_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    full_name: Mapped[str] = mapped_column(String(255))
    
    # "patient", "researcher", "doctor"
    role: Mapped[str] = mapped_column(String(50), default="patient")
    
    # Campos Compartilhados / Onboarding
    institution: Mapped[str | None] = mapped_column(String(255), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Metadados específicos por Role (Orcid para pesquisador, CRM para médico, etc)
    # Assim você não precisa de tabelas novas se quiser adicionar um campo depois
    role_metadata: Mapped[dict | None] = mapped_column(JSONB, default=dict)

    # Dados de Saúde (Apenas para Patients)
    patient_data: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    patient_vector_summary: Mapped[list[float] | None] = mapped_column(
        Vector(384), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    # O researcher_id no ResearchStudy agora aponta direto para User.id
    research_studies: Mapped[list["ResearchStudy"]] = relationship(
        back_populates="researcher",
    )
    patient_statuses: Mapped[list["PatientStatus"]] = relationship(
        back_populates="user",
    )

class ResearchStudy(Base):
    __tablename__ = "research_studies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # FK aponta direto para User.id agora
    researcher_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    nct_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    brief_title: Mapped[str] = mapped_column(String(500))
    official_title: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str | None] = mapped_column(String(100), nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    completion_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    study_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    phase: Mapped[list[str]] = mapped_column(JSONB, default=list)
    conditions: Mapped[list[str]] = mapped_column(JSONB, default=list)
    conditions_normalized: Mapped[list[str]] = mapped_column(JSONB, default=list)
    
    interventions: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    intervention_names: Mapped[list[str]] = mapped_column(JSONB, default=list)

    brief_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    eligibility: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    locations: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    countries: Mapped[list[str]] = mapped_column(JSONB, default=list)
    
    sponsor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_emails: Mapped[list[str]] = mapped_column(JSONB, default=list)
    study_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    study_embedding: Mapped[list[float] | None] = mapped_column(Vector(384), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    researcher: Mapped["User | None"] = relationship(back_populates="research_studies")

class PatientStatus(Base):
    __tablename__ = "patient_statuses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )

    age: Mapped[int | None] = mapped_column(nullable=True)
    sex: Mapped[str | None] = mapped_column(String(10), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)

    medical_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    history: Mapped[str | None] = mapped_column(Text, nullable=True)
    medical_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    conditions: Mapped[list[str]] = mapped_column(JSONB, default=list)
    drugs: Mapped[list[str]] = mapped_column(JSONB, default=list)
    symptoms: Mapped[list[str]] = mapped_column(JSONB, default=list)

    patient_vector_summary: Mapped[list[float] | None] = mapped_column(
        Vector(384), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="patient_statuses")


class SessionEnvironment(Base):
    __tablename__ = "session_environments"
    session_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    environment: Mapped[dict] = mapped_column(JSONB, nullable=False)