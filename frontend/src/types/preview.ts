import type { CardResult } from "./card";

export type PreviewResponse = {
  card: CardResult;
  grayscale_url: string;
  thermal_url: string;
};