from pydantic import BaseModel


class CardResult(BaseModel):
    name: str
    scryfall_id: str
    set_code: str
    collector_number: str
    released_at: str | None = None
    image_url: str
    scryfall_uri: str | None = None