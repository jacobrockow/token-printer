from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.config import PRINTER_HOST, PRINTER_PORT
from app.models.printer import PrintRequest, PrintResponse
from app.services.printer_service import PrinterService

router = APIRouter(prefix="/api", tags=["print"])


@router.post("/print", response_model=PrintResponse)
def print_thermal(request: PrintRequest) -> PrintResponse:
    if not PRINTER_HOST:
        raise HTTPException(status_code=503, detail="Printer is not configured")

    if not request.thermal_url.startswith("/generated/"):
        raise HTTPException(status_code=400, detail="Invalid thermal image path")

    relative_path = request.thermal_url.removeprefix("/generated/")
    absolute_path = Path("app/generated") / relative_path

    if not absolute_path.exists():
        raise HTTPException(status_code=404, detail="Thermal image not found")

    try:
        printer = PrinterService(PRINTER_HOST, PRINTER_PORT)
        printer.print_image(absolute_path)
        return PrintResponse(success=True, message="Print job sent successfully.")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Print failed: {exc}") from exc