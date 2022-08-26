"""
Rest adapter for the Metabase API
"""

import logging
from json import JSONDecodeError
from pathlib import Path
from typing import Optional

from requests import Response, Session
from requests.exceptions import RequestException

from metabase_tools.exceptions import (
    AuthenticationFailure,
    InvalidDataReceived,
    RequestFailure,
)


class MetabaseApi:
    """Metabase API adapter"""

    def __init__(
        self,
        metabase_url: str,
        credentials: Optional[dict] = None,
        cache_token: bool = False,
        token_path: Path | str = Path("./metabase.token"),
    ):
        self._logger = logging.getLogger(__name__)
        authed = False
        credentials = credentials or {}
        token_path = Path(token_path)
        try:
            with open(token_path, "r", encoding="utf-8") as file:
                credentials["token"] = file.read()
        except FileNotFoundError:
            pass

        # Validate Metabase URL
        self.metabase_url = self._validate_base_url(url=metabase_url)

        # Starts session to be reused by the adapter so that the auth token is cached
        self._session = Session()

        # Determines what was supplied in credentials and authenticates accordingly
        if "token" in credentials:
            self._logger.debug("Trying to authenticate with token")
            headers = {
                "Content-Type": "application/json",
                "X-Metabase-Session": credentials["token"],
            }
            authed = (
                200
                <= self._session.get(
                    f"{self.metabase_url}/user/current", headers=headers
                ).status_code
                <= 299
            )
            if authed:
                self._logger.debug("Successfully authenticated with token")
                self._session.headers.update(headers)
            else:
                self._logger.debug("Failed to authenticate with token")
                if token_path.exists():
                    self._logger.debug("Deleting token file")
                    token_path.unlink()

        if not authed and "username" in credentials and "password" in credentials:
            self._logger.debug("Trying to authenticate with username and password")
            self._authenticate(credentials=credentials)
            authed = True

        if not authed:
            raise AuthenticationFailure(
                "Failed to authenticate with credentials provided"
            )

        if cache_token:
            self.save_token(save_path=token_path)

    def _validate_base_url(self, url: str) -> str:
        if url[-1] == "/":
            url = url[:-1]
        if url[-4:] == "/api":
            url = url[:-4]
        if url[:4] != "http":
            url = f"http://{url}"
        return f"{url}/api"

    def _authenticate(self, credentials: dict) -> None:
        """Private method for authenticating a session with the API

        Args:
            credentials (dict): Username and password

        Raises:
            RequestFailure: HTTP error during authentication
            AuthenticationFailure: API responded with failure code
        """
        self._logger.debug("Starting authentication - RestAdapter member")
        try:
            post_request = self._session.post(
                f"{self.metabase_url}/session", json=credentials
            )
        except RequestException as error_raised:
            self._logger.error(str(error_raised))
            raise RequestFailure(
                "Request failed during authentication"
            ) from error_raised

        status_code = post_request.status_code
        if status_code == 200:
            headers = {
                "Content-Type": "application/json",
                "X-Metabase-Session": post_request.json()["id"],
            }
            self._session.headers.update(headers)
            self._logger.debug("Authentication successful")
        else:
            reason = post_request.reason
            raise AuthenticationFailure(
                f"Authentication failed. {status_code} - {reason}"
            )

    def get_token(self) -> str:
        """Get the token being used in the adapter

        Returns:
            str: Token
        """
        return str(self._session.headers.get("X-Metabase-Session"))

    def save_token(self, save_path: Path | str):
        """Writes active token to the specified file

        Args:
            save_path (Path | str): Name of file to write
        """
        token = self.get_token()
        with open(save_path, "w", encoding="utf-8") as file:
            file.write(token)

    def _make_request(
        self,
        method: str,
        url: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> Response:
        """Perform an HTTP request, catching and re-raising any exceptions

        Args:
            method (str): GET or POST or DELETE or PUT
            url (str): URL endpoint
            params (dict, optional): Endpoint parameters
            json (dict, optional): Data payload

        Raises:
            RequestFailure: Request failed

        Returns:
            Response: Response from the API
        """
        log_line_pre = f"{method=}, {url=}, {params=}"
        try:
            self._logger.debug(log_line_pre)
            return self._session.request(
                method=method, url=url, params=params, json=json
            )
        except RequestException as error_raised:
            self._logger.error(str(error_raised))
            raise RequestFailure("Request failed") from error_raised

    def generic_request(
        self,
        http_method: str,
        endpoint: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> list[dict] | dict:
        """Method for dispatching HTTP requests

        Args:
            http_method (str): GET or POST or PUT or DELETE
            endpoint (str): URL endpoint
            params (dict, optional): Endpoint parameters
            json (dict, optional): Data payload

        Raises:
            InvalidDataReceived: Unable to decode response from API
            AuthenticationFailure: Auth failure received from API
            RequestFailure: Other failure during request

        Returns:
            list[dict] | dict: Response from API
        """
        log_line_post = "success=%s, status_code=%s, message=%s"
        response = self._make_request(
            method=http_method,
            url=self.metabase_url + endpoint,
            params=params,
            json=json,
        )

        # If status_code in 200-299 range, return Result, else raise exception
        is_success = 299 >= response.status_code >= 200
        if is_success:
            self._logger.debug(
                log_line_post, is_success, response.status_code, response.reason
            )
            try:
                return response.json()
            except JSONDecodeError as error_raised:
                raise InvalidDataReceived from error_raised
        elif response.status_code == 401:
            self._logger.error(
                log_line_post, False, response.status_code, response.text
            )
            raise AuthenticationFailure(f"{response.status_code} - {response.reason}")

        error_line = f"{response.status_code} - {response.reason}"
        self._logger.error(log_line_post)
        raise RequestFailure(error_line)

    def get(self, endpoint: str, params: Optional[dict] = None) -> list[dict] | dict:
        """HTTP GET request

        Args:
            endpoint (str): URL endpoint
            ep_params (dict, optional): Endpoint parameters

        Returns:
            list[dict] | dict: Response from API
        """
        return self.generic_request(http_method="GET", endpoint=endpoint, params=params)

    def post(
        self, endpoint: str, params: Optional[dict] = None, json: Optional[dict] = None
    ) -> list[dict] | dict:
        """HTTP POST request

        Args:
            endpoint (str): URL endpoint
            params (dict, optional): Endpoint parameters
            json (dict, optional): Data payload

        Returns:
            list[dict] | dict: Response from API
        """
        return self.generic_request(
            http_method="POST", endpoint=endpoint, params=params, json=json
        )

    def delete(self, endpoint: str, params: Optional[dict] = None) -> list[dict] | dict:
        """HTTP DELETE request

        Args:
            endpoint (str): URL endpoint
            params (dict, optional): Endpoint parameters

        Returns:
            list[dict] | dict: Response from API
        """
        return self.generic_request(
            http_method="DELETE", endpoint=endpoint, params=params
        )

    def put(
        self, endpoint: str, params: Optional[dict] = None, json: Optional[dict] = None
    ) -> list[dict] | dict:
        """HTTP PUT request

        Args:
            endpoint (str): URL endpoint
            ep_params (dict, optional): Endpoint parameters
            json (dict, optional): Data payload

        Returns:
            list[dict] | dict: Response from API
        """
        return self.generic_request(
            http_method="PUT", endpoint=endpoint, params=params, json=json
        )
