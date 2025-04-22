from typing import Any

from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
async def info(request: Request) -> dict[str, Any]:
    # Note: reading the body in a GET handler is unusual but possible
    body_bytes = await request.body()

    return {
        # Basic connection data
        "client": {
            "ip": request.client.host,
            "port": request.client.port,
        },
        # URL & routing
        "full_url": str(request.url),
        "path": request.url.path,
        "query_string": request.url.query,
        "method": request.method,
        "http_version": request.scope.get("http_version"),
        # Headers & cookies
        "headers": dict(request.headers),
        "cookies": request.cookies,
        # Body (bytes → str just for demo)
        "raw_body": body_bytes.decode("utf‑8", errors="ignore"),
        # Environment / server info
        "server": request.scope.get("server"),  # (host, port) tuple
        "scheme": request.url.scheme,  # "http" / "https"
        # Anything custom you stashed earlier
        "state": request.state.__dict__,  # e.g. request.state.user_id
    }
