from typing import Any

import httpx
from fastapi import FastAPI, Request

app = FastAPI()

# With httpx (must install it)
import httpx


async def get_geo_info(ip: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://ipapi.co/{ip}/json/")
        return response.json()


@app.get("/")
async def info(request: Request) -> dict[str, Any]:
    # Note: reading the body in a GET handler is unusual but possible
    body_bytes = await request.body()
    user_agent_str = request.headers.get("user-agent", "")
    user_agent = parse(user_agent_str)

    return {
        # Basic connection data
        "client": {
            "ip": request.client.host,
            "port": request.client.port,
            "geo": get_geo_info(request.client.host),
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
        "user_agent": {
            "browser": user_agent.browser.family,
            "browser_version": user_agent.browser.version_string,
            "os": user_agent.os.family,
            "os_version": user_agent.os.version_string,
            "device": user_agent.device.family,
            "is_mobile": user_agent.is_mobile,
            "is_tablet": user_agent.is_tablet,
            "is_pc": user_agent.is_pc,
        },
    }
