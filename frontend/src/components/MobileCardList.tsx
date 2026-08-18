import { useState } from "react";
import { printPreview } from "../api/mobile";
import type { CardResult } from "../types/card";

type MobileCardListProps = {
  results: CardResult[];
};

export default function MobileCardList({ results }: MobileCardListProps) {
  const [printingId, setPrintingId] = useState<string | null>(null);
  const [statusById, setStatusById] = useState<Record<string, string>>({});

  async function handlePrint(card: CardResult) {
    setPrintingId(card.scryfall_id);
    setStatusById((prev) => ({
      ...prev,
      [card.scryfall_id]: "Printing..."
    }));

    try {
      const result = await printPreview(card.scryfall_id, 540);
      setStatusById((prev) => ({
        ...prev,
        [card.scryfall_id]: result.message
      }));
    } catch {
      setStatusById((prev) => ({
        ...prev,
        [card.scryfall_id]: "Print failed."
      }));
    } finally {
      setPrintingId(null);
    }
  }

  if (results.length === 0) {
    return <p className="empty-state">No results yet.</p>;
  }

  return (
    <div className="mobile-card-list">
      {results.map((card) => (
        <article key={card.scryfall_id} className="mobile-card">
          <img
            className="mobile-card-image"
            src={card.image_url}
            alt={card.name}
          />

          <div className="mobile-card-body">
            <div className="card-name">{card.name}</div>
            <div className="card-meta">
              {card.set_code} #{card.collector_number}
            </div>
            <div className="card-meta">
              {card.released_at ?? "Unknown date"}
            </div>

            <button
              className="search-button mobile-print-button"
              onClick={() => handlePrint(card)}
              disabled={printingId === card.scryfall_id}
            >
              {printingId === card.scryfall_id ? "Printing..." : "Print"}
            </button>

            {statusById[card.scryfall_id] && (
              <p className="app-status" style={{ marginTop: "0.5rem" }}>
                {statusById[card.scryfall_id]}
              </p>
            )}
          </div>
        </article>
      ))}
    </div>
  );
}