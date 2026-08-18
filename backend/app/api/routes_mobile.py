from fastapi import APIRouter, HTTPException
from pathlib import Path

from app.config import PRINTER_HOST, PRINTER_PORT
from app.models.printer import PrintResponse
from app.models.preview import PreviewRequest
from app.services.preview_service import PreviewService
from app.services.printer_service import PrinterService

router = APIRouter(prefix="/api", tags=["mobile"])


@router.post("/print-preview", response_model=PrintResponse)
def print_preview(request: PreviewRequest) -> PrintResponse:
    if not PRINTER_HOST:
        raise HTTPException(status_code=503, detail="Printer is not configured")

    try:
        preview_service = PreviewService()
        preview = preview_service.generate_preview(
            scryfall_id=request.scryfall_id,
            width=request.width,
        )

        if not preview.thermal_url.startswith("/generated/"):
            raise HTTPException(status_code=400, detail="Invalid thermal image path")

        relative_path = preview.thermal_url.removeprefix("/generated/")
        absolute_path = Path("app/generated") / relative_path

        if not absolute_path.exists():
            raise HTTPException(status_code=404, detail="Thermal image not found")

        printer = PrinterService(PRINTER_HOST, PRINTER_PORT)
        printer.print_image(absolute_path)

        return PrintResponse(success=True, message="Print job sent successfully.")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Print failed: {exc}") from exc