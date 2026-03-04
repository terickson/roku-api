from typing import Optional

from pydantic import BaseModel


class ActionRequest(BaseModel):
    command: str
    value: Optional[str] = None


class DeviceSummary(BaseModel):
    id: str
    host: str


class AppInfo(BaseModel):
    id: str
    name: str


class DeviceDetail(BaseModel):
    id: str
    host: str
    apps: list[AppInfo]


class ActionResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    message: str
