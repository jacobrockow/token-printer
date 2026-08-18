from pydantic import BaseModel

from app.config import PRINTER_WIDTH
from app.models.card import CardResult


class PreviewRequest(BaseModel):
    scryfall_id: str
    width: int = PRINTER_WIDTH


class PreviewResponse(BaseModel):
    card: CardResult
    grayscale_url: str
    thermal_url: str
