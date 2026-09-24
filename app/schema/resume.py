from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field
from typing import List
from datetime import datetime

# We create schemas for each section of the resume, then put it all together with the resume schema

class Bullet(BaseModel):
  text: str | None = None
  points: List[str]

class Contact(BaseModel):
  first_name: str
  last_name: str
  email: EmailStr
  phone_num: str

class Education(BaseModel):
  qualification: str
  institution: str
  start_date: str | None = None
  end_date: str | None = None
  details: List[Bullet]

class Exprience(BaseModel):
  title: str
  organization: str
  start_date: str
  location: str
  end_date: str | None = None
  details: List[Bullet]

class Skills(BaseModel):
  category: str
  items: List[str]


class ResumeSchema(SQLModel):
  education: List[Education]
  exprience: List[Exprience]
  projects: List[Exprience] # We can use the exprience schema for projects too
  extra: List[Exprience] | None = None
  skills: List[Skills]

class Resume(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  name: str
  contact: dict = Field(sa_column=Column(JSON))
  content: dict = Field(sa_column=Column(JSON))
  updated: datetime = Field(default_factory=datetime.now())