from typing import Union

from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
def read_root(request: Request):
    """
    Inspect the incoming request and return some diagnostic details.
    """
    return {
        "client_ip": request.client.host,  # Source IP address
        "server_host": request.url.hostname,  # Host part of the URL
        "full_url": str(request.url),  # Whole URL that was hit
        "user_agent": request.headers.get("user-agent", "unknown"),
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

    