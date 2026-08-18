import { API_BASE } from "../api/client";
import type { PreviewResponse } from "../types/preview";

type ThermalPreviewPanelProps = {
  preview: PreviewResponse | null;
  loading: boolean;
  status: string;
  onPrint: () => void;
  printLoading: boolean;
  printStatus: string;
};

export default function ThermalPreviewPanel({
  preview,
  loading,
  status,
  onPrint,
  printLoading,
  printStatus
}: ThermalPreviewPanelProps) {
  return (
    <section className="panel">
      <h2>Preview</h2>
      <p className="app-status">{loading ? "Generating preview..." : status}</p>

      {!preview && (
        <p className="empty-state">
          Select a search result to generate a preview.
        </p>
      )}

      {preview && (
        <div className="preview-stack">
          <div>
            <h3 className="preview-subtitle">
              {preview.card.name} — {preview.card.set_code} #
              {preview.card.collector_number}
            </h3>
            <div className="preview-meta">
              Release date: {preview.card.released_at ?? "Unknown"}
            </div>
          </div>

          <div className="preview-grid">
            <div>
              <h3 className="preview-subtitle">Thermal Preview</h3>
              <div className="preview-image-wrap">
                <img
                  className="preview-image"
                  src={`${API_BASE}${preview.thermal_url}`}
                  alt="Thermal preview"
                />
              </div>
            </div>

            <div>
              <h3 className="preview-subtitle">Grayscale Preview</h3>
              <div className="preview-image-wrap">
                <img
                  className="preview-image"
                  src={`${API_BASE}${preview.grayscale_url}`}
                  alt="Grayscale preview"
                />
              </div>
            </div>
          </div>

          <div>
            <button className="search-button" onClick={onPrint} disabled={printLoading}>
              {printLoading ? "Printing..." : "Print Thermal"}
            </button>
            {printStatus && <p className="app-status">{printStatus}</p>}
          </div>

          {preview.card.scryfall_uri && (
            <div>
              <a href={preview.card.scryfall_uri} target="_blank" rel="noreferrer">
                View on Scryfall
              </a>
            </div>
          )}
        </div>
      )}
    </section>
  );
}