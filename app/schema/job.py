from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import List

class Job(BaseModel):
  job_title: str
  company: str
  level: str
  required_skills: List[str]
  preferred_skills: List[str]
  responsibilities: List[str]
  keywords: List[str]

class JobListing(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  job_title: str
  company: str
  url: str