import { API_BASE } from "./client";
import type { PreviewResponse } from "../types/preview";

export async function rollMomir(
  manaValue: number,
  width = 576
): Promise<PreviewResponse> {
  const response = await fetch(`${API_BASE}/api/momir`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      mana_value: manaValue,
      width
    })
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Momir roll failed");
  }

  return response.json();
}
