import time
import uuid

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp, Scope, Receive, Send, Message

EMAIL = "23f3003526@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-e51i9s.example.com"


class RequestHeadersMiddleware:
    """Wrap the entire app so headers also appear on CORS preflight responses."""
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        request_id = str(uuid.uuid4())
        started = time.perf_counter()

        async def send_wrapped(message: Message) -> None:
            if message["type"] == "http.response.start":
                elapsed = max(0.0, time.perf_counter() - started)
                headers = list(message.get("headers", []))
                headers.extend([
                    (b"x-request-id", request_id.encode("ascii")),
                    (b"x-process-time", f"{elapsed:.6f}".encode("ascii")),
                ])
                message["headers"] = headers
            await send(message)

        await self.app(scope, receive, send_wrapped)


api = FastAPI(title="Descriptive Statistics API")
api.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


@api.get("/stats")
def stats(values: str = Query(..., description="Comma-separated integers")):
    parts = values.split(",")
    if any(not part.strip() for part in parts):
        raise HTTPException(status_code=422, detail="values must be comma-separated integers")
    try:
        numbers = [int(part.strip()) for part in parts]
    except ValueError:
        raise HTTPException(status_code=422, detail="values must be comma-separated integers")
    if not numbers:
        raise HTTPException(status_code=422, detail="at least one integer is required")
    total = sum(numbers)
    count = len(numbers)
    return {
        "email": EMAIL,
        "count": count,
        "sum": total,
        "min": min(numbers),
        "max": max(numbers),
        "mean": total / count,
    }


# Outer wrapper ensures request headers are added even when CORS handles OPTIONS itself.
app = RequestHeadersMiddleware(api)
