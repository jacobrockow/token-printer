# Token Printer

Containerized web app for searching Magic: The Gathering cards and tokens, generating thermal-friendly previews, and printing to a network ESC/POS receipt printer.

## Configuration

Copy the example environment file and set the printer address:

```bash
cp .env.example .env
```

At minimum, configure:

```env
PRINTER_HOST=192.168.1.171
PRINTER_PORT=9100
PRINTER_WIDTH=576
```

Do not commit `.env`.

## Development

The development stack runs FastAPI with reload enabled and the Vite development server:

```bash
docker compose up --build
```

The UI is available at `http://localhost:5173`. Vite proxies `/api` and `/generated` requests to the FastAPI backend on port 8000.

## Production deployment

The production stack builds the React frontend into a small Nginx image. Nginx serves the frontend and proxies `/api` and `/generated` to the private FastAPI container, so the application is exposed through a single HTTP port and does not require browser CORS configuration.

Start it with:

```bash
docker compose -f compose.prod.yml up -d --build
```

By default the site is published on host port `8080`. Override this in `.env` if needed:

```env
FRONTEND_PORT=8080
```

Check container status and health with:

```bash
docker compose -f compose.prod.yml ps
```

Follow logs with:

```bash
docker compose -f compose.prod.yml logs -f
```

To update an existing deployment:

```bash
git pull
docker compose -f compose.prod.yml up -d --build
```

## Homelab / reverse proxy

For a VM deployment, point the LAN reverse proxy at the VM's production HTTP port, for example:

```text
http://TOKEN_PRINTER_VM_IP:8080
```

Only the frontend port needs to be reachable from the LAN. The backend remains on the private Docker network and connects directly to `PRINTER_HOST:PRINTER_PORT` when a print job is submitted.

Before testing through the reverse proxy, verify from the VM that the printer is reachable on its raw printing port:

```bash
nc -vz "$PRINTER_HOST" "${PRINTER_PORT:-9100}"
```

## Health endpoint

The backend exposes:

```text
GET /health
```

which returns `{"status":"ok"}` and is used by the production Docker health check.
