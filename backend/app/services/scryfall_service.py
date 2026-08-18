import logging
import re
from typing import Any

import requests

from app.models.card import CardResult

SCRYFALL_API = "https://api.scryfall.com"
USER_AGENT = "token-printer-webapp/0.1"
TIMEOUT = 30

logger = logging.getLogger(__name__)


class ScryfallError(RuntimeError):
    pass


def normalize_query(query: str) -> str:
    normalized = query.strip()
    normalized = re.sub(r"\btoken\b", "", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized or query.strip()

def normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def get_candidate_names(card: dict[str, Any]) -> list[str]:
    names: list[str] = []

    if card.get("name"):
        names.append(str(card["name"]))

    for face in card.get("card_faces", []):
        face_name = face.get("name")
        if face_name:
            names.append(str(face_name))

    return names

def looks_regular(card: dict[str, Any]) -> tuple[int, str]:
    """
    Returns:
      (penalty, reason)
      Lower penalty = more "normal" printing
    """
    # Prefer non-promo, non-variant cards
    if card.get("promo") or card.get("promo_types"):
        return (2, "promo")

    frame_effects = card.get("frame_effects") or []
    if frame_effects:
        return (1, "variant")

    # default = normal printing
    return (0, "regular")

def match_priority(card: dict[str, Any], query: str) -> tuple[int, int, str]:
    """
    Lower is better.
    Sort priority:
      0 = exact full-name match
      1 = exact word-boundary match / startswith
      2 = substring match
      3 = everything else

    Second value prefers more regular prints over promos/showcase/etc.
    Third value keeps newer Scryfall ordering stable-ish by name.
    """
    query_norm = normalize_name(query)
    candidate_names = [normalize_name(name) for name in get_candidate_names(card)]

    regular_penalty, _ = looks_regular(card)

    if any(name == query_norm for name in candidate_names):
        return (0, regular_penalty, candidate_names[0] if candidate_names else "")

    if any(name.startswith(query_norm) for name in candidate_names):
        return (1, regular_penalty, candidate_names[0] if candidate_names else "")

    pattern = rf"\b{re.escape(query_norm)}\b"
    if any(re.search(pattern, name) for name in candidate_names):
        return (1, regular_penalty, candidate_names[0] if candidate_names else "")

    if any(query_norm in name for name in candidate_names):
        return (2, regular_penalty, candidate_names[0] if candidate_names else "")

    return (3, regular_penalty, candidate_names[0] if candidate_names else "")


class ScryfallService:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
            }
        )

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        logger.info("Scryfall GET %s params=%s", path, params)
        response = self.session.get(f"{SCRYFALL_API}{path}", params=params, timeout=TIMEOUT)
        logger.info("Scryfall response status=%s url=%s", response.status_code, response.url)

        if response.status_code == 404:
            return {"object": "list", "data": []}

        response.raise_for_status()
        data = response.json()

        if data.get("object") == "error":
            raise ScryfallError(data.get("details", "Unknown Scryfall API error"))

        return data

    def search_cards(self, query: str, limit: int = 10) -> list[CardResult]:
        normalized = normalize_query(query)
        is_tokenish = "token" in query.lower()

        if is_tokenish:
            fallback_queries = [
                f't:{normalized} game:paper lang:en',
                f'{normalized} t:token game:paper lang:en',
                f'{normalized} game:paper lang:en',
                normalized,
            ]
        else:
            fallback_queries = [
                f'{normalized} game:paper lang:en',
                f'{normalized} t:token game:paper lang:en',
                f't:{normalized} game:paper lang:en',
                normalized,
            ]

        cards: list[dict[str, Any]] = []

        for search_query in fallback_queries:
            logger.info("Trying search query: %s", search_query)
            data = self._get(
                "/cards/search",
                q=search_query,
                unique="prints",
                order="released",
                dir="desc",
                include_extras="true",
            )
            cards = data.get("data", [])
            logger.info("Search query returned %d cards", len(cards))
            if cards:
                break

        if not cards:
            return []

        cards = sorted(cards, key=lambda card: match_priority(card, query))

        results: list[CardResult] = []
        seen_ids: set[str] = set()

        for card in cards:
            card_id = str(card.get("id", ""))
            if not card_id or card_id in seen_ids:
                continue

            image_url = None
            if card.get("image_uris"):
                image_url = card["image_uris"].get("normal") or card["image_uris"].get("large")
            elif card.get("card_faces"):
                for face in card["card_faces"]:
                    image_uris = face.get("image_uris") or {}
                    image_url = image_uris.get("normal") or image_uris.get("large")
                    if image_url:
                        break

            if not image_url:
                continue

            seen_ids.add(card_id)
            results.append(
                CardResult(
                    name=card.get("name", "Unknown Card"),
                    scryfall_id=card_id,
                    set_code=str(card.get("set", "")).upper(),
                    collector_number=str(card.get("collector_number", "")),
                    released_at=card.get("released_at"),
                    image_url=image_url,
                    scryfall_uri=card.get("scryfall_uri"),
                )
            )

            if len(results) >= limit:
                break

        return results

    def get_card_by_id(self, scryfall_id: str) -> dict[str, Any]:
        data = self._get(f"/cards/{scryfall_id}")
        return data

    def extract_image_urls(self, card: dict[str, Any]) -> list[str]:
        image_urls: list[str] = []

        if card.get("image_uris"):
            image_url = card["image_uris"].get("normal") or card["image_uris"].get("large")
            if image_url:
                image_urls.append(image_url)
        else:
            for face in card.get("card_faces", []):
                image_uris = face.get("image_uris") or {}
                image_url = image_uris.get("normal") or image_uris.get("large")
                if image_url:
                    image_urls.append(image_url)

        return image_urls