from pydantic import BaseModel

class OtpAuthSchema(BaseModel):
    email:str
    otp:str
