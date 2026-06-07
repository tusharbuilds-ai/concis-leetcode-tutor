from typing import Optional
from pydantic import BaseModel

class ChatSchem(BaseModel):
    email:str
    session_id:str
    question:str
    query:str
    context: Optional[str]= None

