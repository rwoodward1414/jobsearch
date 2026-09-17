from pydantic import BaseModel
from typing import List

class Job(BaseModel):
  job_title: str
  company: str
  level: str
  required_skills: List[str]
  preferred_skills: List[str]
  responsibilities: List[str]
  keywords: List[str]

