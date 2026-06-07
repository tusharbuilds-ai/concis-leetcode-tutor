from pydantic import BaseModel

class LogoutSchema(BaseModel):
    email:str
    session_id:str