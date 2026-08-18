import { API_BASE } from "./client";

export type PrintResponse = {
  success: boolean;
  message: string;
};

export async function printPreview(
  scryfallId: string,
  width = 540
): Promise<PrintResponse> {
  const response = await fetch(`${API_BASE}/api/print-preview`, {
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
    const text = await response.text();
    throw new Error(text || "Print failed");
  }

  return response.json();
}