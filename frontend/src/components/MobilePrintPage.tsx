import type { FormEvent } from "react";
import { useState } from "react";
import SearchBar from "./SearchBar";
import MobileCardList from "./MobileCardList";
import { searchCards } from "../api/search";
import type { CardResult } from "../types/card";

export default function MobilePrintPage() {
  const [query, setQuery] = useState("");
  const [limit, setLimit] = useState(12);
  const [results, setResults] = useState<CardResult[]>([]);
  const [searchStatus, setSearchStatus] = useState("Search for a card or token.");
  const [searchLoading, setSearchLoading] = useState(false);

  async function handleSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmed = query.trim();
    if (!trimmed) {
      setResults([]);
      setSearchStatus("Search for a card or token.");
      return;
    }

    setSearchLoading(true);
    setSearchStatus("Searching...");

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

  return (
    <main className="app-shell mobile-shell">
      <div className="mobile-search-sticky">
        <h1 className="app-title mobile-title">Token Printer</h1>
        <SearchBar
          query={query}
          loading={searchLoading}
          limit={limit}
          onLimitChange={setLimit}
          onQueryChange={setQuery}
          onSubmit={handleSearch}
        />
        <p className="app-status">{searchStatus}</p>
      </div>

      <MobileCardList results={results} />
    </main>
  );
}