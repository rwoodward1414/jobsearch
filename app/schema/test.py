from pydantic import BaseModel

class Test(BaseModel):
  first_name: str
  last_name: str