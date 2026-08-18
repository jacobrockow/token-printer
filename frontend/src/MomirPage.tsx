import type { FormEvent } from "react";
import { useState } from "react";

import { rollMomir } from "./api/momir";
import { printThermal } from "./api/print";
import ThermalPreviewPanel from "./components/ThermalPreviewPanel";
import type { PreviewResponse } from "./types/preview";
import "./styles/momir.css";

export default function MomirPage() {
  const [manaValue, setManaValue] = useState(1);
  const [preview, setPreview] = useState<PreviewResponse | null>(null);
  const [rollLoading, setRollLoading] = useState(false);
  const [status, setStatus] = useState(
    "Choose a mana value, then roll a random creature and print it."
  );
  const [printLoading, setPrintLoading] = useState(false);
  const [printStatus, setPrintStatus] = useState("");

  async function handlePrint(target = preview) {
    if (!target) return;

    setPrintLoading(true);
    setPrintStatus("Sending print job...");

    try {
      const result = await printThermal(target.thermal_url);
      setPrintStatus(result.message);
    } catch {
      setPrintStatus("Print failed. The rolled card is still available below to retry.");
    } finally {
      setPrintLoading(false);
    }
  }

  async function handleRoll(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setRollLoading(true);
    setPreview(null);
    setPrintStatus("");
    setStatus(`Rolling a random mana value ${manaValue} creature...`);

    try {
      const result = await rollMomir(manaValue);
      setPreview(result);
      setStatus(`Rolled ${result.card.name}.`);
      await handlePrint(result);
    } catch {
      setStatus(`Momir roll failed for mana value ${manaValue}.`);
    } finally {
      setRollLoading(false);
    }
  }

  return (
    <main className="app-shell momir-shell">
      <h1 className="app-title">Momir Printer</h1>
      <p className="app-status">
        Roll a random paper creature with the selected mana value and print it as a token.
      </p>

      <section className="panel momir-controls">
        <form className="momir-form" onSubmit={handleRoll}>
          <label className="momir-label" htmlFor="mana-value">
            Mana value
          </label>
          <input
            id="mana-value"
            className="search-input momir-input"
            type="number"
            min="0"
            max="30"
            step="1"
            value={manaValue}
            onChange={(event) => setManaValue(Number(event.target.value))}
            disabled={rollLoading}
          />
          <button className="search-button" type="submit" disabled={rollLoading}>
            {rollLoading ? "Rolling..." : "Roll & Print"}
          </button>
        </form>
        <p className="app-status">{status}</p>
      </section>

      <div className="momir-preview">
        <ThermalPreviewPanel
          preview={preview}
          loading={rollLoading}
          status={preview ? "Momir result ready." : "No creature rolled yet."}
          onPrint={() => handlePrint()}
          printLoading={printLoading}
          printStatus={printStatus}
        />
      </div>
    </main>
  );
}
