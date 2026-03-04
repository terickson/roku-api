# Roku API

REST API for controlling local Roku devices. Built with FastAPI.

## Setup

### Docker Compose (recommended)

```bash
cp .env.sample .env
# Edit .env with your Roku device IPs
docker compose up --build -d
```

### Local Development

```bash
cp .env.sample .env
# Edit .env with your Roku device IPs
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8080
```

Swagger UI is available at `http://localhost:8080/`.

## Configuration

| Variable | Description | Example |
|---|---|---|
| `LOG_LEVEL` | Logging level | `DEBUG` |
| `LOG_MODULE_NAME` | Logger name | `roku-api` |
| `ROKU_HOSTS` | Comma-separated `name:ip` pairs | `room1:192.168.1.100,room2:192.168.1.101` |
| `HOST` | Bind address | `0.0.0.0` |
| `PORT` | Bind port | `8080` |

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/systems/` | List all configured Roku devices |
| `GET` | `/systems/{id}` | Get device details and installed apps |
| `POST` | `/systems/{id}/actions` | Send a command to a device |

### Supported Commands

`HOME`, `BACK`, `UP`, `DOWN`, `LEFT`, `RIGHT`, `ENTER`, `SELECT`, `PLAY`, `PAUSE`, `FORWARD`, `REVERSE`, `SEARCH`, `INPUT`

Direction commands (`UP`, `DOWN`, `LEFT`, `RIGHT`) accept a `value` field for repeat count. `SEARCH` accepts a `value` for the search term. `INPUT` accepts a `value` for the app ID to launch.

## Tests

```bash
pytest tests/ -v
```
