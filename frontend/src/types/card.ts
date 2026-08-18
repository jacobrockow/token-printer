export type CardResult = {
  name: string;
  scryfall_id: string;
  set_code: string;
  collector_number: string;
  released_at?: string | null;
  image_url: string;
  scryfall_uri?: string | null;
};