import os

PRINTER_HOST = os.environ.get("PRINTER_HOST", "").strip()
PRINTER_PORT = int(os.environ.get("PRINTER_PORT", "9100"))
PRINTER_WIDTH = int(os.environ.get("PRINTER_WIDTH", "576"))
