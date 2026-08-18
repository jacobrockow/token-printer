import type { ChangeEvent, FormEvent } from "react";

type SearchBarProps = {
  query: string;
  loading: boolean;
  limit: number;
  onLimitChange: (value: number) => void;
  onQueryChange: (value: string) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
};

export default function SearchBar({
  query,
  loading,
  limit,
  onLimitChange,
  onQueryChange,
  onSubmit
}: SearchBarProps) {
  return (
    <form onSubmit={onSubmit} className="search-form">
      <input
        className="search-input"
        type="text"
        value={query}
        onChange={(e: ChangeEvent<HTMLInputElement>) =>
          onQueryChange(e.target.value)
        }
        placeholder="Search for a card or token"
      />
      <select
        value={limit}
        onChange={(e) => onLimitChange(Number(e.target.value))}
        style={{
            padding: "12px",
            borderRadius: "12px",
            border: "1px solid var(--border)",
            background: "var(--panel)",
            color: "var(--text)"
        }}
        >
        <option value={6}>6</option>
        <option value={10}>10</option>
        <option value={12}>12</option>
        <option value={20}>20</option>
        <option value={30}>30</option>
      </select>
      <button className="search-button" type="submit" disabled={loading}>
        {loading ? "Searching..." : "Search"}
      </button>
    </form>
  );
}