from sqlmodel import SQLModel, Field
from datetime import datetime

class Application(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  job_id: int | None = Field(default=None, foreign_key="joblisting.id")
  user_id: int | None = Field(default=None, foreign_key="user.id")
  date_applied: datetime
  status: str # TODO make enums for this