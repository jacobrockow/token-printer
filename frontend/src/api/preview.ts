import { API_BASE } from "./client";
import type { PreviewResponse } from "../types/preview";

export async function generatePreview(
  scryfallId: string,
  width = 576
): Promise<PreviewResponse> {
  const response = await fetch(`${API_BASE}/api/preview`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      scryfall_id: scryfallId,
      width
    })
  });

  if (!response.ok) {
    throw new Error("Preview generation failed");
  }

  return response.json();
}