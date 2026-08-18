import type { CardResult } from "../types/card";
import CardTile from "./CardTile";

type CardGridProps = {
  results: CardResult[];
  selectedCardId?: string;
  onSelect: (card: CardResult) => void;
};

export default function CardGrid({
  results,
  selectedCardId,
  onSelect
}: CardGridProps) {
  if (results.length === 0) {
    return <p className="empty-state">No results to display yet.</p>;
  }

  return (
    <div className="card-grid">
      {results.map((card) => (
        <CardTile
          key={card.scryfall_id}
          card={card}
          selected={selectedCardId === card.scryfall_id}
          onClick={() => onSelect(card)}
        />
      ))}
    </div>
  );
}