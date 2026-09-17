from pydantic import BaseModel

class Resume(BaseModel):
  first_name: str
  last_name: str
  
