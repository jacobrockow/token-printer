from pathlib import Path

from app.models.card import CardResult
from app.models.preview import PreviewResponse
from app.services.image_service import ImageService
from app.services.scryfall_service import ScryfallService


class PreviewService:
    def __init__(self) -> None:
        self.scryfall = ScryfallService()
        self.images = ImageService()
        self.output_dir = Path("app/generated/previews")

    def generate_preview(self, scryfall_id: str, width: int = 576) -> PreviewResponse:
        card = self.scryfall.get_card_by_id(scryfall_id)

        image_urls = self.scryfall.extract_image_urls(card)
        face_images = [self.images.download_image(url) for url in image_urls]

        combined = self.images.combine_faces(face_images)
        combined = self.images.autocontrast_with_border(combined)

        grayscale = self.images.resize_for_width(combined, width)
        grayscale = self.images.maybe_lighten(grayscale)

        thermal = self.images.dither_to_bw(grayscale)

        grayscale_filename = f"{scryfall_id}_gray.png"
        thermal_filename = f"{scryfall_id}_thermal.png"

        grayscale_path = self.output_dir / grayscale_filename
        thermal_path = self.output_dir / thermal_filename

        self.images.save_image(grayscale, grayscale_path)
        self.images.save_image(thermal, thermal_path)

        card_result = CardResult(
            name=card.get("name", "Unknown Card"),
            scryfall_id=str(card.get("id", "")),
            set_code=str(card.get("set", "")).upper(),
            collector_number=str(card.get("collector_number", "")),
            released_at=card.get("released_at"),
            image_url=image_urls[0],
            scryfall_uri=card.get("scryfall_uri"),
        )

        return PreviewResponse(
            card=card_result,
            grayscale_url=f"/generated/previews/{grayscale_filename}",
            thermal_url=f"/generated/previews/{thermal_filename}",
        )