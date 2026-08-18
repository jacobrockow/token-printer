from pydantic import BaseModel


class PrintRequest(BaseModel):
    thermal_url: str


class PrintResponse(BaseModel):
    success: bool
    message: str