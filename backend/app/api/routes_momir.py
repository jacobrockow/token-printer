from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.config import PRINTER_WIDTH
from app.models.preview import PreviewResponse
from app.services.preview_service import PreviewService
from app.services.scryfall_service import ScryfallService

router = APIRouter(prefix="/api", tags=["momir"])


class MomirRequest(BaseModel):
    mana_value: int = Field(ge=0, le=30)
    width: int = PRINTER_WIDTH


@router.post("/momir", response_model=PreviewResponse)
def roll_momir(request: MomirRequest) -> PreviewResponse:
    scryfall = ScryfallService()
    card = scryfall._get(
        "/cards/random",
        q=f"t:creature mv:{request.mana_value} game:paper lang:en",
    )

    scryfall_id = str(card.get("id", ""))
    if not scryfall_id:
        raise HTTPException(
            status_code=404,
            detail=f"No paper creature found with mana value {request.mana_value}",
        )

    return PreviewService().generate_preview(
        scryfall_id=scryfall_id,
        width=request.width,
    )
