import { API_BASE } from "./client";
import type { CardResult } from "../types/card";

export async function searchCards(query: string, limit = 10): Promise<CardResult[]> {
  const response = await fetch(
    `${API_BASE}/api/search?q=${encodeURIComponent(query)}&limit=${limit}`
  );

  if (!response.ok) {
    throw new Error("Search failed");
  }

  return response.json();
}