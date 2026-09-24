from pydantic import BaseModel

class Critique(BaseModel):
    issues: str
    flagged: bool
