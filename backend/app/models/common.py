from pydantic import BaseModel, Field
from typing import Optional


class Message(BaseModel):
    role: str = Field(..., description="Role of the sender: 'user' or 'assistant'")
    content: str = Field(..., description="Content of the message")


class Citation(BaseModel):
    title: str
    url: Optional[str] = None
    ref_code: str
