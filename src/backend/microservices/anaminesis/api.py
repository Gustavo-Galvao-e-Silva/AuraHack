from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from anamnesis import AnamnesisAgent
from schemas import PatientSummary
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "anamnesis_app"

session_service = InMemorySessionService()
runner: Runner = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global runner
    runner = Runner(
        agent=AnamnesisAgent(),
        app_name=APP_NAME,
        session_service=session_service,
    )
    yield


app = FastAPI(lifespan=lifespan)


# --- Request / Response schemas ---

class StartRequest(BaseModel):
    user_id: str
    session_id: str
    initial_goals: list[str] | None = None

class MessageRequest(BaseModel):
    user_id: str
    session_id: str
    message: str

class MessageResponse(BaseModel):
    reply: str
    complete: bool

class SessionResponse(BaseModel):
    complete: bool

class ReportResponse(BaseModel):
    conditions: list[str]
    drugs: list[str]
    description: str
    history: str
    medical_notes: str
    symptoms: list[str]
    medical_summary: str

# --- Endpoints ---
import base64
from fastapi import File, UploadFile
from agents import doctor, summarizer, checker_agent, task_factory, report_agent, pdf_report_agent

@app.post("/report/pdf", response_model=ReportResponse)
async def report_from_pdfs(files: list[UploadFile] = File(...)):
    """Generate a medical report from one or more uploaded PDF documents."""

    if not files:
        raise HTTPException(status_code=400, detail="No files provided.")

    # Build content parts — one document block per PDF
    parts = []
    for file in files:
        if not file.content_type == "application/pdf":
            raise HTTPException(
                status_code=400,
                detail=f"{file.filename} is not a PDF."
            )
        raw = await file.read()
        b64 = base64.standard_b64encode(raw).decode("utf-8")
        parts.append(
            types.Part(
                inline_data=types.Blob(
                    mime_type="application/pdf",
                    data=b64,
                )
            )
        )

    # Add instruction as final text part
    parts.append(types.Part(text="Analyze the documents and generate the medical report."))

    # Use a temporary session for this stateless call
    temp_user = f"pdf_user_{id(files)}"
    temp_session = f"pdf_session_{id(files)}"

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=temp_user,
        session_id=temp_session,
        state={},
    )

    pdf_runner = Runner(
        agent=pdf_report_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    events = [event async for event in pdf_runner.run_async(
        user_id=temp_user,
        session_id=temp_session,
        new_message=types.Content(
            role="user",
            parts=parts,
        ),
    )]

    # Extract result
    result: MedicalReport | None = None
    for event in events:
        if hasattr(event, "data") and isinstance(event.data, MedicalReport):
            result = event.data
        elif event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    try:
                        result = MedicalReport(**json.loads(part.text.strip()))
                    except Exception:
                        pass

    # Clean up temp session
    await session_service.delete_session(
        app_name=APP_NAME,
        user_id=temp_user,
        session_id=temp_session,
    )

    if result is None:
        raise HTTPException(status_code=500, detail="Failed to generate report from PDFs.")

    return ReportResponse(
        conditions=result.conditions,
        drugs=result.drugs,
        description=result.description,
        history=result.history,
        medical_notes=result.medical_notes,
        symptoms=result.symptoms,
        medical_summary=result.medical_summary,
    )

@app.post("/session/{user_id}/{session_id}/report", response_model=ReportResponse)
async def generate_report(user_id: str, session_id: str):
    """Generate a medical report if the session is complete."""
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    if session.state.get("current_goals"):
        raise HTTPException(
            status_code=400,
            detail="Anamnesis is not complete yet. Finish the conversation first."
        )

    # Run the report agent
    report_runner = Runner(
        agent=report_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    events = [event async for event in report_runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=types.Content(
            role="user",
            parts=[types.Part(text="Generate the medical report.")],
        ),
    )]

    # Extract result
    result: MedicalReport | None = None
    for event in events:
        if hasattr(event, "data") and isinstance(event.data, MedicalReport):
            result = event.data
        elif event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    try:
                        result = MedicalReport(**json.loads(part.text.strip()))
                    except Exception:
                        pass

    if result is None:
        raise HTTPException(status_code=500, detail="Failed to generate report.")

    return ReportResponse(
        conditions=result.conditions,
        drugs=result.drugs,
        description=result.description,
        history=result.history,
        medical_notes=result.medical_notes,
        symptoms=result.symptoms,
        medical_summary=result.medical_summary,
    )

@app.post("/session/start")
async def start_session(req: StartRequest):
    """Create a new patient session."""
    goals = req.initial_goals or [
        "Determine duration of symptoms",
        "Check for history of allergies",
        "Confirm if pain is localized",
        "Determine patient age",
        "Determine which country patient is from",
        "Figure out the patient's occupation",
    ]

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=req.user_id,
        session_id=req.session_id,
        state={
            "current_goals": goals,
            "patient_summary": PatientSummary(
                findings_summary="",
                confidence_score=0.0,
            ),
            "awaiting_patient": False,
            "last_patient_message": "",
            "last_doctor_message": "",
        },
    )
    return {"status": "session created", "session_id": req.session_id}


@app.post("/message", response_model=MessageResponse)
async def send_message(req: MessageRequest):
    """Send a patient message and get the doctor's reply."""
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=req.user_id,
        session_id=req.session_id,
    )
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found. Call /session/start first.")

    # Write patient message to state before running
    session.state["last_patient_message"] = req.message

    reply_parts = []
    async for event in runner.run_async(
        user_id=req.user_id,
        session_id=req.session_id,
        new_message=types.Content(
            role="user",
            parts=[types.Part(text=req.message)],
        ),
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    # Filter out raw JSON responses from summarizer/factory
                    try:
                        import json
                        json.loads(part.text.strip())
                        # If it parses as JSON, skip it
                        continue
                    except Exception:
                        pass
                    if event.author == "doctor" or event.author == "anamnesis":
                        reply_parts.append(part.text)

    # Fetch updated session state
    updated = await session_service.get_session(
        app_name=APP_NAME,
        user_id=req.user_id,
        session_id=req.session_id,
    )
    current_goals = updated.state.get("current_goals", [])

    return MessageResponse(
        reply="\n".join(reply_parts),
        complete=len(current_goals) == 0,
    )


@app.get("/session/{user_id}/{session_id}", response_model=SessionResponse)
async def get_session(user_id: str, session_id: str):
    """Get the current state of a session."""
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    summary = session.state.get("patient_summary")
    current_goals = session.state.get("current_goals", [])

    return SessionResponse(
        complete=len(current_goals) == 0,
    )


@app.delete("/session/{user_id}/{session_id}")
async def delete_session(user_id: str, session_id: str):
    """Delete a session."""
    await session_service.delete_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )
    return {"status": "deleted"}
