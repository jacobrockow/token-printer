from pydantic import BaseModel

from app.models.card import CardResult


class PreviewRequest(BaseModel):
    scryfall_id: str
    width: int = 576


class PreviewResponse(BaseModel):
    card: CardResult
    grayscale_url: str
    thermal_url: str