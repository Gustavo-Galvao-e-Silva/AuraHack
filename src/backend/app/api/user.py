from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, PatientStatus

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/health")
def user_routes_health():
    return {"status": "ok"}


class PatientVectorUpdate(BaseModel):
    vector: list[float]


@router.patch("/{user_id}/patient-vector")
def update_patient_vector_for_user(
    user_id: int,
    payload: PatientVectorUpdate,
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    patient_status = db.execute(
        select(PatientStatus)
        .where(PatientStatus.user_id == user_id)
        .order_by(PatientStatus.created_at.desc())
    ).scalars().first()

    if not patient_status:
        raise HTTPException(status_code=404, detail="Patient status not found for this user")

    patient_status.patient_vector_summary = payload.vector

    db.commit()
    db.refresh(patient_status)

    return {
        "status": "ok",
        "message": "Patient vector updated",
        "patient_status_id": patient_status.id,
        "user_id": user_id,
    }