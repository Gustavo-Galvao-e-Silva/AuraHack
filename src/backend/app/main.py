from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Researcher
from .schemas import (
    ResearcherCreate,
    ResearcherOut,
    PaperCreate,
    PaperOut,
)

app = FastAPI()

Base.metadata.create_all(bind=engine)


