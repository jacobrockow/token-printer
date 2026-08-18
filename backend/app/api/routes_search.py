from fastapi import APIRouter, Query

from app.models.card import CardResult
from app.services.scryfall_service import ScryfallService

router = APIRouter(prefix="/api", tags=["search"])


@router.get("/search", response_model=list[CardResult])
def search_cards(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50)
) -> list[CardResult]:
    service = ScryfallService()
    return service.search_cards(q, limit=limit)