from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Researcher, Paper
from .schemas import (
    ResearcherCreate,
    ResearcherOut,
    PaperCreate,
    PaperOut,
)

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/researchers", response_model=ResearcherOut)
def create_researcher(payload: ResearcherCreate, db: Session = Depends(get_db)):
    existing = db.execute(
        select(Researcher).where(Researcher.clerk_user_id == payload.clerk_user_id)
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=409, detail="Researcher already exists")

    researcher = Researcher(
        clerk_user_id=payload.clerk_user_id,
        orcid_id=payload.orcid_id,
        full_name=payload.full_name,
        email=payload.email,
    )
    db.add(researcher)
    db.commit()
    db.refresh(researcher)
    return researcher


@app.get("/researchers/{researcher_id}", response_model=ResearcherOut)
def get_researcher(researcher_id: int, db: Session = Depends(get_db)):
    researcher = db.get(Researcher, researcher_id)
    if not researcher:
        raise HTTPException(status_code=404, detail="Researcher not found")
    return researcher


@app.post("/researchers/{researcher_id}/papers", response_model=PaperOut)
def create_paper(
    researcher_id: int,
    payload: PaperCreate,
    db: Session = Depends(get_db),
):
    researcher = db.get(Researcher, researcher_id)
    if not researcher:
        raise HTTPException(status_code=404, detail="Researcher not found")

    paper = Paper(
        researcher_id=researcher_id,
        title=payload.title,
        abstract=payload.abstract,
        doi=payload.doi,
    )
    db.add(paper)
    db.commit()
    db.refresh(paper)
    return paper


@app.get("/researchers/{researcher_id}/papers", response_model=list[PaperOut])
def list_papers(researcher_id: int, db: Session = Depends(get_db)):
    researcher = db.get(Researcher, researcher_id)
    if not researcher:
        raise HTTPException(status_code=404, detail="Researcher not found")

    papers = db.execute(
        select(Paper).where(Paper.researcher_id == researcher_id)
    ).scalars().all()

    return papers