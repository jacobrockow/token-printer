# Token Printer

Containerized web app for searching Magic: The Gathering cards and tokens, generating thermal-friendly previews, and printing to a network receipt printer.

## Setup

```bash
cp .env.example .env
```

Set `PRINTER_HOST` in `.env` to your printer's LAN address. Do not commit `.env`.

```bash
docker compose up --build
```

The UI defaults to http://localhost:5173 and the API to http://localhost:8000.
