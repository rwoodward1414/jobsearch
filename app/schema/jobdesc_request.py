from pydantic import BaseModel

class JobDescRequest(BaseModel):
  url: str
