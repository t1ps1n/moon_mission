import logging
import time
from uuid import uuid4

from data_classes import CommandRequest, CommandResponse, RobotStatus
from database import get_async_session
from fastapi import Depends, FastAPI, Request, Security
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from settings import API_TOKEN
from utils import add_command, get_current_position

app = FastAPI()

security = HTTPBearer(auto_error=False)

logger = logging.getLogger("api_logger")


@app.middleware("http")
async def token_middleware(request: Request, call_next):
    if request.url.path in ("/docs", "/openapi.json"):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"detail": "Authorization header missing or invalid"},
        )

    token = auth_header.split("Bearer ")[1]
    if token != API_TOKEN:
        return JSONResponse(status_code=401, content={"detail": "Invalid token"})

    response = await call_next(request)
    return response


@app.middleware("http")
async def log_requests(request: Request, call_next):
    uid = str(uuid4())

    start_time = time.time()
    logger.info(f"Incoming request {uid}: {request.method} {request.url}")

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    logger.info(
        f"Completed response {uid}: {request.method} {request.url} with status "
        f"{response.status_code} in {process_time:.2f} ms"
    )

    return response


@app.get("/status", response_model=RobotStatus, dependencies=[Security(security)])
async def get_status(async_session=Depends(get_async_session)):
    x, y, direction, status, command_id = await get_current_position(async_session)
    return RobotStatus(
        x=x,
        y=y,
        direction=direction,
        status=status,
        command_id=command_id,
    )


@app.post(
    "/command",
    response_model=CommandResponse,
    dependencies=[Security(security)],
)
async def register_command(
    command: CommandRequest, async_session=Depends(get_async_session)
):
    command = await add_command(async_session, command)
    return CommandResponse(id=command.id)
