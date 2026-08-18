import os

PRINTER_HOST = os.environ.get("PRINTER_HOST", "").strip()
PRINTER_PORT = int(os.environ.get("PRINTER_PORT", "9100"))
PRINTER_WIDTH = int(os.environ.get("PRINTER_WIDTH", "576"))
SCRYFALL_USER_AGENT = os.environ.get("SCRYFALL_USER_AGENT", "token-printer-webapp/0.1").strip()
