class Result:
    """Result returned from RestAdapter
    Args:
        status_code (int): Standard HTTP status code
        message (str, optional): Human readable result. Defaults to ''.
        data (list[dict], optional): Data payload from response. Defaults to None.
    """

    status_code: int
    message: str = ""
    data: list[dict] | dict | None  # TODO make Result.data always a list of dicts

    def __init__(
        self, status_code: int, message: str = "", data: list[dict] | dict | None = None
    ):
        self.status_code = status_code
        self.message = message
        self.data = data
