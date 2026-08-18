import type { CardResult } from "../types/card";

type CardTileProps = {
  card: CardResult;
  selected: boolean;
  onClick: () => void;
};

export default function CardTile({
  card,
  selected,
  onClick
}: CardTileProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`card-tile${selected ? " selected" : ""}`}
    >
      <img src={card.image_url} alt={card.name} />
      <div className="card-name">{card.name}</div>
      <div className="card-meta">
        {card.set_code} #{card.collector_number}
      </div>
      <div className="card-meta">{card.released_at ?? "Unknown date"}</div>
    </button>
  );
}