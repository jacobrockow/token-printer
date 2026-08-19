import type { FormEvent } from "react";
import { useRef, useState } from "react";
import SearchBar from "./components/SearchBar";
import CardGrid from "./components/CardGrid";
import ThermalPreviewPanel from "./components/ThermalPreviewPanel";
import { searchCards } from "./api/search";
import { generatePreview } from "./api/preview";
import { printThermal } from "./api/print";
import type { CardResult } from "./types/card";
import type { PreviewResponse } from "./types/preview";

export default function DesktopApp() {
  const [query, setQuery] = useState("");
  const [limit, setLimit] = useState(12);
  const [results, setResults] = useState<CardResult[]>([]);
  const [searchStatus, setSearchStatus] = useState("Enter a search term.");
  const [searchLoading, setSearchLoading] = useState(false);

  const [selectedCard, setSelectedCard] = useState<CardResult | null>(null);
  const [preview, setPreview] = useState<PreviewResponse | null>(null);
  const [previewStatus, setPreviewStatus] = useState(
    "Select a card to generate a preview."
  );
  const [previewLoading, setPreviewLoading] = useState(false);

  const [printLoading, setPrintLoading] = useState(false);
  const [printStatus, setPrintStatus] = useState("");
  const previewRef = useRef<HTMLDivElement>(null);

  async function handleSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmed = query.trim();
    if (!trimmed) {
      setResults([]);
      setSelectedCard(null);
      setPreview(null);
      setSearchStatus("Enter a search term.");
      return;
    }

    setSearchLoading(true);
    setSearchStatus("Searching...");
    setSelectedCard(null);
    setPreview(null);
    setPrintStatus("");
    setPreviewStatus("Select a card to generate a preview.");

    try {
      const data = await searchCards(trimmed, limit);
      setResults(data);
      setSearchStatus(
        data.length ? `Found ${data.length} result(s).` : "No results found."
      );
    } catch {
      setResults([]);
      setSearchStatus("Search failed.");
    } finally {
      setSearchLoading(false);
    }
  }

  function focusPreviewOnMobile() {
    if (!window.matchMedia("(max-width: 700px)").matches) return;

    requestAnimationFrame(() => {
      previewRef.current?.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });
    });
  }

  async function handleSelect(card: CardResult) {
    setSelectedCard(card);
    setPreview(null);
    setPrintStatus("");
    setPreviewLoading(true);
    setPreviewStatus("Generating preview...");
    focusPreviewOnMobile();

    try {
      const data = await generatePreview(card.scryfall_id, 540);
      setPreview(data);
      setPreviewStatus("Preview ready.");
    } catch {
      setPreview(null);
      setPreviewStatus("Preview generation failed.");
    } finally {
      setPreviewLoading(false);
    }
  }

  async function handlePrint() {
    if (!preview) return;

    setPrintLoading(true);
    setPrintStatus("Sending print job...");

    try {
      const result = await printThermal(preview.thermal_url);
      setPrintStatus(result.message);
    } catch {
      setPrintStatus("Print failed.");
    } finally {
      setPrintLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <h1 className="app-title">Token Printer</h1>

      <SearchBar
        query={query}
        loading={searchLoading}
        limit={limit}
        onLimitChange={setLimit}
        onQueryChange={setQuery}
        onSubmit={handleSearch}
      />

      <p className="app-status">{searchStatus}</p>

      <div className={`layout-grid${selectedCard ? " has-selection" : ""}`}>
        <section className="panel results-panel">
          <h2>Search Results</h2>
          <CardGrid
            results={results}
            selectedCardId={selectedCard?.scryfall_id}
            onSelect={handleSelect}
          />
        </section>

        <div className="preview-column" ref={previewRef}>
          <ThermalPreviewPanel
            preview={preview}
            loading={previewLoading}
            status={previewStatus}
            onPrint={handlePrint}
            printLoading={printLoading}
            printStatus={printStatus}
          />
        </div>
      </div>
    </main>
  );
}
