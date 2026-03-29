from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
# Importe o schema de saída do User ou mantenha o PatientStatusOut se ele bater com os campos
from app.schemas import PatientStatusCreate, UserOut 

router = APIRouter(prefix="/patient-status", tags=["patient-statuses"])

@router.post("/", response_model=UserOut)
def update_patient_medical_info(
    payload: PatientStatusCreate,
    db: Session = Depends(get_db),
):
    # 1. Buscar o usuário pelo ID (Integer interno)
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Atualizar os campos principais que agora estão no User
    user.location = payload.location
    user.bio = payload.description # Usando bio como o 'description' geral

    # 3. Organizar os dados médicos dentro do JSONB 'patient_data'
    user.patient_data = {
        "sex": payload.sex,
        "age": payload.age,
        "history": payload.history,
        "medical_notes": payload.medical_notes,
        "medical_summary": payload.medical_summary,
        "conditions": payload.conditions,
        "drugs": payload.drugs,
        "symptoms": payload.symptoms,
    }

    db.commit()
    db.refresh(user)

    return user