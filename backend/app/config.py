import os

PRINTER_HOST = os.environ.get("PRINTER_HOST", "").strip()
PRINTER_PORT = int(os.environ.get("PRINTER_PORT", "9100"))
PRINTER_WIDTH = int(os.environ.get("PRINTER_WIDTH", "576"))
PRINTER_DPI = int(os.environ.get("PRINTER_DPI", "203"))
PRINT_BOTTOM_MARGIN_MM = float(os.environ.get("PRINT_BOTTOM_MARGIN_MM", "30"))
CUT_AFTER_PRINT = os.environ.get("CUT_AFTER_PRINT", "false").strip().lower() in {"1", "true", "yes", "on"}
THERMAL_BRIGHTNESS_NORMAL = float(os.environ.get("THERMAL_BRIGHTNESS_NORMAL", "1.10"))
THERMAL_BRIGHTNESS_DARK = float(os.environ.get("THERMAL_BRIGHTNESS_DARK", "1.20"))
SCRYFALL_USER_AGENT = os.environ.get("SCRYFALL_USER_AGENT", "token-printer-webapp/0.1").strip()
