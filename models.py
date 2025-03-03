from pydantic import BaseModel

class SOAPRequest(BaseModel):
    soap_text: str
