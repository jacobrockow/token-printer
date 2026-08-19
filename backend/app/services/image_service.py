import io
from pathlib import Path

import requests
from PIL import Image, ImageOps, ImageStat

from app.config import (
    SCRYFALL_USER_AGENT,
    THERMAL_BRIGHTNESS_DARK,
    THERMAL_BRIGHTNESS_NORMAL,
)


class ImageService:
    def __init__(self, timeout: int = 15) -> None:
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": SCRYFALL_USER_AGENT,
                "Accept": "image/avif,image/webp,image/*,*/*;q=0.8",
            }
        )

    def download_image(self, url: str) -> Image.Image:
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content)).convert("L")

    def combine_faces(self, images: list[Image.Image], gap: int = 24) -> Image.Image:
        if len(images) == 1:
            return images[0]

        width = max(img.width for img in images)
        height = sum(img.height for img in images) + gap * (len(images) - 1)
        canvas = Image.new("L", (width, height), color=255)

        y = 0
        for img in images:
            x = (width - img.width) // 2
            canvas.paste(img, (x, y))
            y += img.height + gap

        return canvas

    def autocontrast_with_border(self, image: Image.Image, border: int = 16) -> Image.Image:
        bordered = ImageOps.expand(image, border=border, fill=255)
        return ImageOps.autocontrast(bordered)

    def resize_for_width(self, image: Image.Image, width: int) -> Image.Image:
        ratio = width / image.width
        height = max(1, round(image.height * ratio))
        return image.resize((width, height), Image.Resampling.LANCZOS)

    def lighten_for_thermal(self, image: Image.Image) -> Image.Image:
        mean = ImageStat.Stat(image).mean[0]
        factor = THERMAL_BRIGHTNESS_DARK if mean < 110 else THERMAL_BRIGHTNESS_NORMAL
        return image.point(lambda p: min(255, int(p * factor)))

    def dither_to_bw(self, image: Image.Image) -> Image.Image:
        return image.convert("1", dither=Image.Dither.FLOYDSTEINBERG)

    def save_image(self, image: Image.Image, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        image.save(path)
