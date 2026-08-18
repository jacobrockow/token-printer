import socket
from pathlib import Path

from PIL import Image


class PrinterService:
    def __init__(self, host: str, port: int = 9100) -> None:
        self.host = host
        self.port = port

    def _image_to_escpos_raster(self, image: Image.Image) -> bytes:
        """
        Convert a 1-bit PIL image into ESC/POS raster format using GS v 0.
        """
        if image.mode != "1":
            image = image.convert("1")

        width, height = image.size
        width_bytes = (width + 7) // 8
        padded_width = width_bytes * 8

        if padded_width != width:
            padded = Image.new("1", (padded_width, height), 1)
            padded.paste(image, (0, 0))
            image = padded
            width = padded_width

        data = bytearray()

        # GS v 0
        # 1D 76 30 m xL xH yL yH d1...dk
        xL = width_bytes & 0xFF
        xH = (width_bytes >> 8) & 0xFF
        yL = height & 0xFF
        yH = (height >> 8) & 0xFF

        data.extend(b"\x1d\x76\x30\x00")
        data.extend(bytes([xL, xH, yL, yH]))

        pixels = image.load()

        for y in range(height):
            for xb in range(width_bytes):
                byte = 0
                for bit in range(8):
                    x = xb * 8 + bit
                    pixel = pixels[x, y]
                    # In mode "1", black is 0 and white is 255/1 depending on access path.
                    is_black = pixel == 0
                    if is_black:
                        byte |= 1 << (7 - bit)
                data.append(byte)

        return bytes(data)

    def print_image(self, image_path: str | Path) -> None:
        image_path = Path(image_path)

        with Image.open(image_path) as img:
            image = img.convert("1")
            payload = bytearray()

            payload.extend(b"\x1b@")  # Initialize
            payload.extend(b"\x1ba\x01")  # Center alignment
            payload.extend(self._image_to_escpos_raster(image))
            payload.extend(b"\n\n\n")
            payload.extend(b"\x1d\x56\x00")  # Full cut

        with socket.create_connection((self.host, self.port), timeout=5) as sock:
            sock.sendall(payload)