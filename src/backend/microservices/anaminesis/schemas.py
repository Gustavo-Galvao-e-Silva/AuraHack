from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class DFAState(str, Enum):
    INTERVIEW = "interview"
    RESEARCH = "research"
    FINISH = "finish"

class GoalCheck(BaseModel):
    goal_index: int
    satisfied: bool = Field(description="True if the patient summary contains this info.")

class NewTasks(BaseModel):
    added_tasks: List[str] = Field(
        default_factory=list, 
        description="New clinical goals discovered during the conversation."
    )

class PatientSummary(BaseModel):
    findings_summary: str = Field(description="The consolidated medical SOAP note.")
    confidence_score: float = Field(description="How certain we are of the data (0.0-1.0).")

class Handshake(BaseModel):
    """The main object passed between major state transitions"""
    next_state: DFAState
    current_tasks: List[str]

class MedicalReport(BaseModel):
    conditions: List[str] = Field(default_factory=list)
    drugs: List[str] = Field(default_factory=list)
    description: str
    history: str
    medical_notes: str
    symptoms: List[str] = Field(default_factory=list)
    medical_summary: str
