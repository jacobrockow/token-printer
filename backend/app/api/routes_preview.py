from fastapi import APIRouter

from app.models.preview import PreviewRequest, PreviewResponse
from app.services.preview_service import PreviewService

router = APIRouter(prefix="/api", tags=["preview"])


@router.post("/preview", response_model=PreviewResponse)
def create_preview(request: PreviewRequest) -> PreviewResponse:
    service = PreviewService()
    return service.generate_preview(
        scryfall_id=request.scryfall_id,
        width=request.width,
    )