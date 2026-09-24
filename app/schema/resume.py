from pydantic import BaseModel, EmailStr
from typing import List

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


class Resume(BaseModel):
  name: str # This is the name of the resume to track versions, not the users name
  contact: Contact
  education: List[Education]
  exprience: List[Exprience]
  projects: List[Exprience] # We can use the exprience schema for projects too
  extra: List[Exprience] | None = None
  skills: List[Skills]
