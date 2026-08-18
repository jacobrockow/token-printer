import { API_BASE } from "./client";

export type PrintResponse = {
  success: boolean;
  message: string;
};

export async function printThermal(thermalUrl: string): Promise<PrintResponse> {
  const response = await fetch(`${API_BASE}/api/print`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      thermal_url: thermalUrl
    })
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Print failed");
  }

  return response.json();
}