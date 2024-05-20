from typing import Optional

from pydantic import BaseModel, Field

from sais.notify.types import NotifyType


class NotificationRequest(BaseModel):
    notify_type: NotifyType
    to: str
    message: str


class MessageModel(BaseModel):
    message: str
    to: str
    type: Optional[str]
    robot_name: Optional[str] = Field(default=None, alias='robotName', description='Robot name field')
