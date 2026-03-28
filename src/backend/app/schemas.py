from pydantic import BaseModel, EmailStr, ConfigDict


class PaperCreate(BaseModel):
    title: str
    abstract: str | None = None
    doi: str | None = None


class PaperOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    abstract: str | None
    doi: str | None


class ResearcherCreate(BaseModel):
    clerk_user_id: str
    orcid_id: str | None = None
    full_name: str
    email: EmailStr | None = None


class ResearcherOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    clerk_user_id: str
    orcid_id: str | None
    full_name: str
    email: str | None