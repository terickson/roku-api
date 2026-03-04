import logging
from time import sleep

from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from roku import Roku

from lib.config import settings
from models.roku import (
    ActionRequest,
    ActionResponse,
    DeviceDetail,
    DeviceSummary,
    ErrorResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/systems", tags=["Systems"])

DIRECTION_COMMANDS = {"UP": "up", "DOWN": "down", "LEFT": "left", "RIGHT": "right"}


def _get_devices() -> list[dict]:
    return settings.get_roku_devices()


def _get_lookup() -> dict[str, str]:
    return settings.get_roku_lookup()


def _run_command_x_times(roku: Roku, times: int, method: str):
    for _ in range(times):
        getattr(roku, method)()
        sleep(1)


@router.get("/", response_model=list[DeviceSummary])
def list_systems():
    return _get_devices()


@router.get("/{device_id}", response_model=DeviceDetail, responses={404: {"model": ErrorResponse}})
def get_system(device_id: str):
    lookup = _get_lookup()
    logger.info("get roku %s", device_id)
    if device_id not in lookup:
        return JSONResponse(status_code=404, content={"message": "Device not found"})
    roku = Roku(lookup[device_id])
    apps = [{"id": app.id, "name": app.name} for app in roku.apps]
    return {"id": device_id, "host": lookup[device_id], "apps": apps}


@router.post(
    "/{device_id}/actions",
    response_model=ActionResponse,
    status_code=201,
    responses={404: {"model": ErrorResponse}, 412: {"model": ErrorResponse}},
)
def create_action(device_id: str, action: ActionRequest):
    lookup = _get_lookup()
    logger.info("post roku action for: %s", device_id)
    if device_id not in lookup:
        return JSONResponse(status_code=404, content={"message": "Device not found"})

    roku = Roku(lookup[device_id])
    command = action.command.upper()
    logger.info("action: %s", action.model_dump())

    if command == "HOME":
        roku.home()
    elif command == "BACK":
        roku.back()
    elif command in DIRECTION_COMMANDS:
        times = int(action.value) if action.value else 1
        _run_command_x_times(roku, times, DIRECTION_COMMANDS[command])
    elif command == "ENTER":
        roku.enter()
    elif command == "SELECT":
        roku.select()
    elif command in ("PLAY", "PAUSE"):
        roku.play()
    elif command == "FORWARD":
        roku.forward()
    elif command == "REVERSE":
        roku.reverse()
    elif command == "SEARCH":
        search_term = action.value.lower() if action.value else ""
        roku.search()
        roku.literal(search_term)
    elif command == "INPUT":
        app = roku[action.value]
        app.launch()
    else:
        return JSONResponse(
            status_code=412,
            content={"message": f"Action command {command} could not be found."},
        )

    return JSONResponse(status_code=201, content={"message": "success"})
