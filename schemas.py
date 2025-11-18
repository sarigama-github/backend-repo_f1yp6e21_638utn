from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class Contact(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    message: str = Field(..., min_length=5, max_length=5000)

class CaseStudy(BaseModel):
    title: str
    impact: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = []
