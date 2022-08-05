from pydantic import BaseModel  # TODO: Remove
from pydantic.fields import Field


class Result(BaseModel):
    """Result returned from RestAdapter
    Args:
        status_code (int): Standard HTTP status code
        message (str, optional): Human readable result. Defaults to ''.
        data (list[dict], optional): Data payload from response. Defaults to None.
    """
    status_code: int
    message: str = ''
    data: list[dict] | dict | None = Field(default_factory=list)
